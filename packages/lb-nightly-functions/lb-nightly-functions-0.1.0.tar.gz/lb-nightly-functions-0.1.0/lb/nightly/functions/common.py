###############################################################################
# (c) Copyright 2020 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import asyncio
import json
import logging
import os
import socket
from collections import namedtuple
from contextlib import redirect_stderr
from datetime import datetime, timezone
from io import StringIO
from shutil import copyfileobj
from subprocess import CalledProcessError, run
from tempfile import NamedTemporaryFile
from zlib import decompress

from git import GitCommandError
from lb.nightly.configuration import DataProject, Package, Project


class Report:
    """
    Class used to collect reports.

    Record messages and forward them to a logger.

    Apart from normal logging levels, accept extra type of messages, like
    ``git_error``.
    """

    def __init__(self, logger=__name__):
        self.logger = logging.getLogger(logger)
        self.records = []

    def log(self, type, level, fmt, args=None):
        record = {"type": type, "level": level, "text": (fmt % args if args else fmt)}
        if type in ("error", "warning") and f"{type}:" not in record["text"]:
            record["text"] = "{}: {}".format(type, record["text"])
        self.records.append(record)
        getattr(self.logger, level)(fmt, *(() if args is None else args))

    def debug(self, fmt, *args):
        self.log("debug", "debug", fmt, args)

    def info(self, fmt, *args):
        self.log("info", "info", fmt, args)

    def warning(self, fmt, *args):
        self.log("warning", "warning", fmt, args)

    warn = warning

    def error(self, fmt, *args):
        self.log("error", "error", fmt, args)

    def git_error(self, msg, err: GitCommandError):
        """
        Special handling for GitCommandError
        """
        self.warning("%s: GitCommand status %s", msg, err.status)
        # FIXME: this is very much subject to the internal details of GitCommandError
        self.log("command", "debug", "> %s", (err._cmdline,))
        if "'" in err.stdout:
            self.log(
                "stdout", "debug", err.stdout[err.stdout.index("'") + 1 : -1].rstrip()
            )
        if "'" in err.stderr:
            self.log(
                "stderr", "debug", err.stderr[err.stderr.index("'") + 1 : -1].rstrip()
            )

    def md(self):
        """
        Format as markdown.
        """
        out = []
        if hasattr(self, "project"):
            out.append("# {name}/{version}".format(**self.project))
        for r in self.records:
            lines = r["text"].splitlines()
            if r["type"] in ("stdout", "stderr", "command"):
                out.append("  ```")
                out.extend("  " + l for l in lines)
                out.append("  ```")
            else:
                out.append("- " + lines.pop(0))
                out.extend("  " + l for l in lines)
        if hasattr(self, "packages"):
            out.extend(pkg.md() for pkg in self.packages)
        return "\n".join(out)

    def __str__(self):
        out = []
        if hasattr(self, "project"):
            out.append("{name}/{version}".format(**self.project))
            out.append("-" * len(out[-1]))
            out.append("")
        out.extend(r["text"] for r in self.records)
        if hasattr(self, "packages"):
            out.extend(str(pkg) for pkg in self.packages)
        return "\n".join(out)

    def to_dict(self):
        from copy import deepcopy

        data = deepcopy(self.__dict__)
        data["logger"] = self.logger.name
        if "packages" in data:
            data["packages"] = [pkg.to_dict() for pkg in data["packages"]]

        return data


def ensure_dir(path, rep: Report):
    """
    Make sure that a directory exist, creating it
    and passing a warning to Report object if dir does not exist.
    """
    if not os.path.exists(path):
        rep.warning(f"directory {path} is missing, I create it")
        os.makedirs(path)


def find_path(name, search_path=None):
    """
    Look for a file or directory in a search path.

    If the search path is not specified, the concatenation of CMTPROJECTPATH
    and CMAKE_PREFIX_PATH is used.

    >>> find_path('true', ['/usr/local/bin', '/bin'])
    '/bin/true'
    >>> print(find_path('cannot_find_me', []))
    None
    """
    from os import environ, pathsep
    from os.path import exists, join

    if search_path is None:
        search_path = environ.get("CMAKE_PREFIX_PATH", "").split(pathsep) + environ.get(
            "CMTPROJECTPATH", ""
        ).split(pathsep)

    try:
        return next(
            join(path, name) for path in search_path if exists(join(path, name))
        )
    except StopIteration:
        logging.warning("%s not found in %r", name, search_path)
    return None


def get_build_method(project=None):
    """
    Helper function to get a build method for a project.

    The method is looked up in the following order: build_tool property of a project,
    build_tool property of a slot owning the project, the default build method (cmake).

    If a method is retrieved via build_tool string property, it must be defined in
    lb.nightly.functions.build.
    """
    import lb.nightly.functions.build as build_methods

    try:
        method = project.build_tool or project.slot.build_tool
        return getattr(build_methods, method)
    except (AttributeError, TypeError):
        return build_methods.cmake


def safe_dict(mydict):
    """Helper to return the dictionary without sensitive data
    To be used e.g. to remove secret environment variables.
    >>> d={"PASSWORD": "my_secret_pass", "PASS": "asd", "USER": "me", "KEY": "asd", "TOKEN": "asd", "PRIVATE": "Asd", "HOME": "Asd", "SHA": "asd"}
    >>> safe_dict(d)
    {}
    """
    return {
        k: v
        for k, v in mydict.items()
        if all(
            s not in k.upper()
            for s in [
                "PASS",
                "USER",
                "KEY",
                "TOKEN",
                "PRIVATE",
                "HOME",
                "SHA",
            ]
        )
    }


cernvm = {
    "slc5": "/cvmfs/cernvm-prod.cern.ch/cvm3",
    "slc6": "/cvmfs/cernvm-prod.cern.ch/cvm4",
    "centos7": "/cvmfs/cernvm-prod.cern.ch/cvm4",
}


def singularity_run(
    cmd,
    env={},
    cwd=os.getcwd(),
    task={},
    krb_auth=None,
    use_lbenv=True,
):
    from spython.main import Client

    try:
        os_id = env["BINARY_TAG"].split("-")[1]
        Client.load(cernvm[os_id])
    except KeyError:
        raise EnvironmentError(
            f"Could not find the CernVM image for the "
            f"{env.get('BINARY_TAG', 'not specified BINARY_TAG')}"
        )

    s_env = {
        k: env.get(k)
        for k in ("PATH", "CMAKE_PREFIX_PATH", "BINARY_TAG", "CMTCONFIG", "LCG_VERSION")
        if k in env
    }
    s_env.update(env)
    s_env = safe_dict(s_env)

    # specify workspace in container
    workspace_singularity = "/workspace"
    pwd = workspace_singularity
    if cwd != os.getcwd():
        cwd = os.path.join(workspace_singularity, cwd)
        pwd = cwd

    # patch PATH and CMAKE_PREFIX_PATH to work in container
    try:
        s_env["PATH"] = s_env["PATH"].replace(os.getcwd(), workspace_singularity)
        s_env["CMAKE_PREFIX_PATH"] = s_env["CMAKE_PREFIX_PATH"].replace(
            os.getcwd(), workspace_singularity
        )
    except KeyError:
        pass

    if krb_auth:
        krb_token = NamedTemporaryFile()
        s_env["KRB5CCNAME"] = f"FILE:{krb_token.name}"

        class KerberosAuthenticationError(Exception):
            pass

        try:
            run(
                ["kinit", "-c", krb_token.name, krb_auth[0]],
                input=krb_auth[1].encode(),
                check=True,
            )
        except (CalledProcessError, IndexError):
            raise KerberosAuthenticationError(
                "Could not authenticate with provided credentials"
            )

    # setting up elasticsearch where we send logs from singularity
    from elasticsearch import Elasticsearch
    from lb.nightly.configuration import service_config

    conf = service_config()
    es_url = conf.get("elasticsearch", {}).get("uri")
    ca_certs = conf.get("elasticsearch", {}).get("ca_certs")
    index_pattern_prefix = conf.get("elasticsearch", {}).get(
        "index_pattern_prefix",
        "lhcb-core-logs-nightlies",
    )
    elastic = Elasticsearch(
        [es_url],
        use_ssl=True,
        verify_certs=True,
        ca_certs=ca_certs,
    )
    logging.getLogger("elasticsearch").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    if elastic.ping():
        # stub of the msg to sent to elasticsearch
        log_body = {
            "host": socket.gethostname(),
            "command": cmd,
            "cwd": cwd,
            "task": task.get("task"),
            "project": task.get("project"),
            "platform": task.get("platform"),
            "worker_task_id": task.get("worker_task_id"),
            "log": None,  # will be overriden just before sending
            "timestamp": None,  # same as above
        }
        log_body.update(
            {
                "log": f"Running command: {cmd} with env: {s_env}",
                "timestamp": datetime.now(timezone.utc),
            }
        )
        elastic.index(
            index=f"{index_pattern_prefix}-{datetime.now(timezone.utc).strftime('%Y.%d.%m')}-{task.get('task', 'nightlies')}",
            body=log_body,
        )

    if "TASK_LOGFILE" in env:
        with open(env.get("TASK_LOGFILE"), "a") as logfile:
            logfile.write(
                f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}: "
                f"Running command: {cmd} with {s_env}\n"
            )

    # to collect the build messages we communicate through the UNIX socket
    from hashlib import sha256

    hash = sha256()
    hash.update(f"{cmd} {task} {cwd}".encode())
    os.environ["LB_WRAPCMD_SOCKET"] = s_env["LB_WRAPCMD_SOCKET"] = os.path.join(
        "/tmp", hash.hexdigest()[:32]
    )

    Result = namedtuple(
        "Result",
        [
            "returncode",
            "stdout",
            "stderr",
            "args",
            "build_logs",
        ],
    )

    script_cmd = NamedTemporaryFile()
    if use_lbenv:
        script_cmd.write(b"source /cvmfs/lhcb.cern.ch/lib/LbEnv-unstable\n")
        script_cmd.write(b"export PATH=$PATH:" + s_env.pop("PATH").encode() + b"\n")
        script_cmd.write(
            b"export CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH:"
            + s_env.pop("CMAKE_PREFIX_PATH").encode()
            + b"\n"
        )
    script_cmd.write((" ".join(cmd) + "\n").encode())
    script_cmd.seek(0)

    try:
        result = Client.execute(
            ["sh", script_cmd.name],
            bind=[
                "/cvmfs",
                env.get("CONDA_ENV"),
                f"{os.getcwd()}:{workspace_singularity}",
            ],
            options=[f"--pwd={pwd}", "--cleanenv"]
            + [f"--env={k}={v}" for k, v in s_env.items()],
            stream=True,
        )

        stdout = b""
        build_logs = {}

        async def get_stdout(result):
            nonlocal stdout
            for line in result:
                stdout += line.encode(errors="surrogateescape")
                yield line
                await asyncio.sleep(0)

        async def log_to_file(result):
            with open(
                os.environ.get("TASK_LOGFILE"),
                "a",
                buffering=512,
            ) as logfile:
                async for line in result:
                    logfile.write(
                        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}: "
                        f"{line.rstrip()}\n"
                    )
                    yield line
                    await asyncio.sleep(0)

        async def log_to_elastic(result):
            async for line in result:
                yield dict(
                    log_body,
                    **{
                        "_index": f"{index_pattern_prefix}-{datetime.now(timezone.utc).strftime('%Y.%d.%m')}-{task.get('task', 'nightlies')}",
                        "log": line.rstrip(),
                        "timestamp": datetime.now(timezone.utc),
                    },
                )
                await asyncio.sleep(0)

        from elasticsearch import AsyncElasticsearch
        from elasticsearch.helpers import async_streaming_bulk

        aelastic = AsyncElasticsearch(
            [es_url],
            use_ssl=True,
            verify_certs=True,
            ca_certs=ca_certs,
        )

        async def stream_to_elastic(result):
            async for _ in async_streaming_bulk(
                aelastic,
                result,
                chunk_size=100,
            ):
                await asyncio.sleep(0)

        async def stream_to_file(result):
            async for _ in log_to_file(result):
                await asyncio.sleep(0)

        if "TASK_LOGFILE" in env:

            async def get_output_and_log(result):
                if elastic.ping():
                    await stream_to_elastic(
                        log_to_elastic(log_to_file(get_stdout(result)))
                    )
                else:
                    await stream_to_file(get_stdout(result))

        else:

            async def get_output_and_log(result):
                if elastic.ping():
                    await stream_to_elastic(log_to_elastic(get_stdout(result)))
                else:
                    await stream_to_file(get_stdout(result))

        async def read_from_singularity(result):
            nonlocal stdout
            await get_output_and_log(result)
            return stdout

        server_address = os.environ["LB_WRAPCMD_SOCKET"]
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise

        async def _receive(reader, writer):
            buffer = b""
            while True:
                msg = await reader.read(4096)
                if msg:
                    buffer += msg
                else:
                    break
            data = json.loads(decompress(buffer))
            build_logs.setdefault(data.pop("subdir"), {}).setdefault(
                data.pop("target"), []
            ).append(data)

        async def read_socket(server_address):
            server = await asyncio.start_unix_server(
                _receive,
                server_address,
            )
            async with server:
                try:
                    await server.serve_forever()
                except asyncio.exceptions.CancelledError:
                    pass

        async def main_get_read(result, server_address):
            nonlocal stdout
            asyncio.create_task(read_socket(server_address))
            task = asyncio.create_task(read_from_singularity(result))
            try:
                await task
            except asyncio.exceptions.CancelledError:
                pass
            return stdout

        with redirect_stderr(StringIO()) as singularity_stderr:
            stdout = asyncio.run(main_get_read(result, server_address))

        # will be overwritten if CalledProcessError is raised
        retcode = 0

    except CalledProcessError as cpe:
        retcode = cpe.returncode
    finally:
        try:
            os.unlink(server_address)
        except OSError:
            pass
        try:
            del os.environ["LB_WRAPCMD_SOCKET"]
        except KeyError:
            pass
        try:
            krb_token.close()
        except NameError:
            pass
        script_cmd.close()
    return Result(
        stdout=stdout,
        returncode=retcode,
        stderr=singularity_stderr.getvalue().encode(errors="surrogateescape"),
        args=cmd,
        build_logs=build_logs,
    )


async def write_to_socket(socket_name, message):
    _, writer = await asyncio.open_unix_connection(socket_name)
    writer.write(message)
    writer.close()


def lb_wrapcmd():
    """
    The script to be used in CMake launcher rules.

    A launcher rule defined as
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE "lb-wrapcmd <CMAKE_CURRENT_BINARY_DIR> <TARGET_NAME>")

    Output for each compile command is sent to the socket
    (name taken from LB_WRAPCMD_SOCKET env variable or built as:
    <CMAKE_CURRENT_BINARY_DIR>/1234-<TARGET_NAME>-abc-build.log)
    """
    import sys
    from argparse import REMAINDER, ArgumentParser
    from shutil import which
    from time import time
    from zlib import compress

    parser = ArgumentParser()
    parser.add_argument("log_dir", help="CMAKE_CURRENT_BINARY_DIR")
    parser.add_argument("target", help="TARGET_NAME")
    parser.add_argument("wrap_cmd", nargs=REMAINDER, help="wrapped command")
    args = parser.parse_args()

    with NamedTemporaryFile() as statistics_file:
        time_cmd = [
            which("time"),
            "-f",
            '{"duration": "%E", "maxresident": "%M", "avgresident": "%t", "cpupercentage": "%P"}',
            "-o",
            statistics_file.name,
        ]
        started = time()
        result = run(time_cmd + args.wrap_cmd, capture_output=True)
        completed = time()
        sys.stdout.buffer.write(result.stdout)
        sys.stderr.buffer.write(result.stderr)

        if "LB_WRAPCMD_SOCKET" in os.environ:
            server_address = os.environ["LB_WRAPCMD_SOCKET"]

            output = {
                "subdir": "/".join(args.log_dir.split("/")[4:]),
                "target": args.target,
                "cmd": args.wrap_cmd,
                "stdout": "",
                "stderr": "",
                "returncode": result.returncode,
                "started": started,
                "completed": completed,
            }
            statistics_file.seek(0)
            with open(statistics_file.name, "r") as f:
                statistics = json.loads(f.read())
            output.update(statistics)

            if args.wrap_cmd[0] != "cat":
                output["stdout"] = result.stdout.decode(errors="surrogateescape")
                output["stderr"] = result.stderr.decode(errors="surrogateescape")

            asyncio.run(
                write_to_socket(server_address, compress(json.dumps(output).encode()))
            )

    return result.returncode


def download_and_unzip(repo, artifact):
    """
    Helper function to download the artifact
    and unzip it in the current directory.

    :param repo: ArtifactsRepository object to get the artifact from
    :param artifact: the value returned by the `artifacts`
    method of the Project.

    Returns True if succeded.
    """
    try:
        with NamedTemporaryFile() as lp:
            with repo.pull(artifact) as remote:
                copyfileobj(remote, lp)
            lp.seek(0)
            return not run(["unzip", "-o", lp.name], check=True).returncode
    except Exception:
        return False


def get_artifacts_list(project, platform, stage="build"):
    """
    Helper function returning the list of the artifcts
    needed to perform `stage` (build or test) for `project` and `platform`
    """
    artifacts = []
    if stage in ["build", "test"]:
        artifacts.append(project.artifacts("checkout"))
        if stage == "test":
            artifacts.append(project.artifacts("build", platform))
        for dep_name in project.dependencies():
            if dep_name in project.slot.projects:
                dependency = project.slot.projects[dep_name]
                if dependency.enabled:
                    if isinstance(dependency, (Package, DataProject)):
                        artifacts.append(dependency.artifacts("checkout"))
                    elif isinstance(dependency, Project):
                        artifacts.append(dependency.artifacts("build", platform))
    return artifacts
