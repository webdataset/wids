from collections import namedtuple
from io import BytesIO, IOBase
from mmap import mmap
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

# Type definition for TarHeader
TarHeader = namedtuple('TarHeader', [
    'name', 'mode', 'uid', 'gid', 'size', 'mtime', 'chksum', 'typeflag',
    'linkname', 'magic', 'version', 'uname', 'gname', 'devmajor', 'devminor', 'prefix'
])

# Type aliases
FileContentType = bytes
FilePath = str
FileDescriptor = int
CleanupCallbackType = Callable[[Optional[FilePath], FileDescriptor, str], None]

# Functions
def parse_tar_header(header_bytes: bytes) -> TarHeader: ...
def next_header(offset: int, header: TarHeader) -> int: ...
def keep_while_reading(fname: Optional[FilePath], fd: FileDescriptor, phase: str, delay: float = 0.0) -> None: ...

# Classes
class MMIndexedTar:
    verbose: bool
    cleanup_callback: Optional[CleanupCallbackType]
    stream: IOBase
    fname: Optional[FilePath]
    mmapped_file: mmap
    by_name: Dict[str, int]
    by_index: List[Tuple[str, int, int]]
    
    def __init__(
        self, 
        fname: Union[FilePath, IOBase], 
        index_file: Optional[Callable] = None, 
        verbose: bool = True, 
        cleanup_callback: Optional[CleanupCallbackType] = None
    ) -> None: ...
    
    def close(self, dispose: bool = False) -> None: ...
    def _build_index(self) -> None: ...
    def names(self) -> Iterator[str]: ...
    def get_at_offset(self, offset: int) -> Tuple[str, FileContentType]: ...
    def get_at_index(self, index: int) -> Tuple[str, FileContentType]: ...
    def get_by_name(self, name: str) -> Tuple[str, FileContentType]: ...
    def __iter__(self) -> Iterator[Tuple[str, FileContentType]]: ...
    def __getitem__(self, key: Union[int, str]) -> Tuple[str, FileContentType]: ...
    def __len__(self) -> int: ...
    def get_file(self, i: int) -> Tuple[str, BytesIO]: ...