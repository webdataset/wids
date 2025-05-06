import fcntl
import os
import shutil
import subprocess
import sys
import time
from collections import deque
from datetime import datetime
from urllib.parse import urlparse

recent_downloads = deque(maxlen=1000)

open_objects = {}
max_open_objects = 100


class ULockFile:
    """A simple locking class. We don't need any of the third
    party libraries since we rely on POSIX semantics for linking
    below anyway."""

    def __init__(self, path):
        self.lockfile_path = path
        self.lockfile = None

    def __enter__(self):
        self.lockfile = open(self.lockfile_path, "w")
        fcntl.flock(self.lockfile.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        fcntl.flock(self.lockfile.fileno(), fcntl.LOCK_UN)
        self.lockfile.close()
        self.lockfile = None
        try:
            os.unlink(self.lockfile_path)
        except FileNotFoundError:
            pass


def pipe_download(remote, local):
    """Perform a download for a pipe: url."""
    if not remote.startswith("pipe:"):
        raise ValueError(f"Invalid pipe URL: {remote}")
    cmd = remote[5:]
    cmd = cmd.format(local=local)
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.decode('utf-8', errors='replace')
        raise RuntimeError(f"Command failed: {cmd}, error: {stderr}")


def copy_file(remote, local):
    parsed_remote = urlparse(remote)
    if parsed_remote.scheme not in ["file", ""]:
        raise ValueError(f"Unsupported remote scheme: {parsed_remote.scheme}")
    # Convert remote URL to absolute file path
    remote_path = os.path.abspath(parsed_remote.path)
    # Parse and validate local URL
    parsed_local = urlparse(local)
    if parsed_local.scheme not in ["file", ""]:
        raise ValueError(f"Unsupported local scheme: {parsed_local.scheme}")
    local_path = os.path.abspath(parsed_local.path)
    # If remote and local paths are identical, do nothing
    if remote_path == local_path:
        return
    # Copy the remote file to local path
    shutil.copyfile(remote_path, local_path)


verbose_cmd = int(os.environ.get("WIDS_VERBOSE_CMD", "0"))


def vcmd(flag, verbose_flag=""):
    return verbose_flag if verbose_cmd else flag


def download_http(url, local):
    """Download a file using curl for HTTP/HTTPS."""
    args = ["curl"]
    if not verbose_cmd:
        args.append("-s")
    args.extend(["-L", url, "-o", local])
    result = subprocess.run(args, check=True, capture_output=True)
    return result.returncode == 0


def download_ftp(url, local):
    """Download a file using curl for FTP/FTPS."""
    args = ["curl"]
    if not verbose_cmd:
        args.append("-s")
    args.extend(["-L", url, "-o", local])
    result = subprocess.run(args, check=True, capture_output=True)
    return result.returncode == 0


def download_gs(url, local):
    """Download a file from Google Cloud Storage."""
    args = ["gsutil"]
    if not verbose_cmd:
        args.append("-q")
    args.extend(["cp", url, local])
    result = subprocess.run(args, check=True, capture_output=True)
    return result.returncode == 0


def download_s3(url, local):
    """Download a file from Amazon S3."""
    args = ["aws", "s3", "cp", url, local]
    result = subprocess.run(args, check=True, capture_output=True)
    return result.returncode == 0


default_cmds = {
    "posixpath": copy_file,
    "file": copy_file,
    "pipe": pipe_download,
    "http": download_http,
    "https": download_http,
    "ftp": download_ftp,
    "ftps": download_ftp,
    "gs": download_gs,
    "s3": download_s3,
}


def download_file_no_log(remote, local, handlers=default_cmds):
    """Download a file from a remote url to a local path.
    The remote url can be a pipe: url, in which case the remainder of
    the url is treated as a command template that is executed to perform the download.
    """

    if remote.startswith("pipe:"):
        schema = "pipe"
    else:
        schema = urlparse(remote).scheme
    if schema is None or schema == "":
        schema = "posixpath"
    # get the handler
    handler = handlers.get(schema)
    if handler is None:
        raise ValueError("Unknown schema: %s" % schema)
    # call the handler - all handlers are now callable functions
    handler(remote, local)
    return local


def download_file(remote, local, handlers=default_cmds, verbose=False):
    start = time.time()
    try:
        return download_file_no_log(remote, local, handlers=handlers)
    finally:
        recent_downloads.append((remote, local, time.time(), time.time() - start))
        if verbose:
            print(
                "downloaded",
                remote,
                "to",
                local,
                "in",
                time.time() - start,
                "seconds",
                file=sys.stderr,
            )


def download_and_open(remote, local, mode="rb", handlers=default_cmds, verbose=False):
    with ULockFile(local + ".lock"):
        if not os.path.exists(local):
            if verbose:
                print("downloading", remote, "to", local, file=sys.stderr)
            download_file(remote, local, handlers=handlers)
        else:
            if verbose:
                print("using cached", local, file=sys.stderr)
        result = open(local, mode)
        if open_objects is not None:
            for k, v in list(open_objects.items()):
                if v.closed:
                    del open_objects[k]
            if len(open_objects) > max_open_objects:
                raise RuntimeError("Too many open objects")
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            key = tuple(str(x) for x in [remote, local, mode, current_time])
            open_objects[key] = result
        return result
