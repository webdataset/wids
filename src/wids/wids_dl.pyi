from collections import deque
from datetime import datetime
from io import BufferedReader, BufferedRandom, BufferedWriter, TextIOWrapper
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import subprocess

# Type aliases
FilePath = str
URL = str
DownloadHandler = Callable[[URL, FilePath], Any]
HandlersType = Dict[str, DownloadHandler]

# Module level variables
recent_downloads: deque[Tuple[URL, FilePath, float, float]]
open_objects: Dict[Tuple[str, ...], Union[BufferedReader, BufferedWriter, BufferedRandom, TextIOWrapper]]
max_open_objects: int
verbose_cmd: int

class ULockFile:
    lockfile_path: str
    lockfile: Optional[TextIOWrapper]
    
    def __init__(self, path: str) -> None: ...
    def __enter__(self) -> 'ULockFile': ...
    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], 
                exc_tb: Optional[Any]) -> None: ...

def pipe_download(remote: str, local: str) -> None: ...
def copy_file(remote: str, local: str) -> None: ...
def vcmd(flag: str, verbose_flag: str = "") -> str: ...

def download_http(url: str, local: str) -> bool: ...
def download_ftp(url: str, local: str) -> bool: ...
def download_gs(url: str, local: str) -> bool: ...
def download_s3(url: str, local: str) -> bool: ...

default_cmds: HandlersType

def download_file_no_log(remote: str, local: str, 
                         handlers: HandlersType = default_cmds) -> str: ...
def download_file(remote: str, local: str, 
                  handlers: HandlersType = default_cmds, 
                  verbose: bool = False) -> str: ...
def download_and_open(remote: str, local: str, 
                      mode: str = "rb", 
                      handlers: HandlersType = default_cmds, 
                      verbose: bool = False) -> Union[BufferedReader, BufferedWriter, BufferedRandom, TextIOWrapper]: ...