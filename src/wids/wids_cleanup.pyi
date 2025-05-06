from typing import List, Optional, Tuple
from multiprocessing import Process
import fcntl
import os

def keep_most_recent_files(
    pattern: str, 
    maxsize: int = int(1e12), 
    maxfiles: int = 1000, 
    debug: bool = False
) -> None: ...

class ExclusiveLock:
    lockfile: str
    lock: Optional[os.PathLike]
    
    def __init__(self, lockfile: str) -> None: ...
    def try_lock(self) -> bool: ...
    def release_lock(self) -> None: ...

def create_cleanup_background_process(
    pattern: str, 
    maxsize: int = int(1e12), 
    maxfiles: int = 1000, 
    every: int = 60
) -> Process: ...