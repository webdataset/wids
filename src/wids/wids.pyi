from typing import Any, BinaryIO, Callable, Dict, Generic, Iterator, List, Optional, Protocol, Sequence, Tuple, TypeVar, Union, overload
from io import BufferedReader, BytesIO
import numpy as np
import sqlite3
import uuid

# Import from other wids modules
from .wids_lru import LRUCache
from .wids_mmtar import MMIndexedTar
from .wids_tar import TarFileReader

# Type variables
T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

# Type aliases
FilePath = str
URL = str
SampleType = Dict[str, Any]
SampleIndices = List[int]
SampleTransform = Callable[[Dict[str, Any]], Dict[str, Any]]

# Functions
def compute_file_md5sum(fname: Union[str, BinaryIO], chunksize: int = 1000000) -> str: ...
def compute_num_samples(fname: str) -> int: ...
def splitname(fname: str) -> Tuple[str, str]: ...
def group_by_key(names: List[str]) -> List[List[int]]: ...
def hash_localname(dldir: str = "/tmp/_wids_cache") -> Callable[[str], str]: ...

# Classes
class IndexedTarSamples:
    path: Optional[str]
    stream: BufferedReader
    reader: Union[MMIndexedTar, TarFileReader]
    samples: List[List[int]]
    uuid: str
    
    def __init__(
        self,
        *,
        path: Optional[str] = None,
        stream: Optional[BufferedReader] = None,
        md5sum: Optional[str] = None,
        expected_size: Optional[int] = None,
        use_mmap: bool = True,
        index_file: Callable = ...,
    ) -> None: ...
    
    def close(self) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, idx: int) -> SampleType: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class CacheLocalname:
    _cachedir: str
    
    def __init__(self, cachedir: str) -> None: ...
    def __call__(self, shard: str) -> str: ...

class DefaultLocalname:
    _dldir: str
    
    def __init__(self, dldir: str = "/tmp/_wids_cache") -> None: ...
    def __call__(self, shard: str) -> str: ...

class LRUShards:
    localname: Callable[[str], str]
    lru: LRUCache
    accesses: int
    misses: int
    last_missed: bool
    
    def __init__(
        self, 
        lru_size: int, 
        keep: bool = False, 
        localname: Callable[[str], str] = ...,
    ) -> None: ...
    
    def reset_stats(self) -> None: ...
    def __len__(self) -> int: ...
    def release_handler(self, key: str, value: IndexedTarSamples) -> None: ...
    def clear(self) -> None: ...
    def get_shard(self, url: str) -> IndexedTarSamples: ...

class ShardListDataset(Generic[T]):
    shards: List[Dict[str, Any]]
    localname: Callable[[str], str]
    cache: LRUShards
    lengths: List[int]
    total_length: int
    decoder: Callable[[bytes, str], Any]
    shard_index_fn: Callable[[int], Tuple[int, int]]
    _transformations: List[SampleTransform]
    
    def __init__(
        self,
        shards: Union[str, List[Dict[str, Any]]],
        lru_size: int = 30,
        download: bool = True,
        localname: Optional[Callable[[str], str]] = None,
        verbose: bool = False,
        decoder: Callable[[bytes, str], Any] = ...,
    ) -> None: ...
    
    def set_transformations(self, transformations: List[SampleTransform]) -> 'ShardListDataset[T]': ...
    def add_transformation(self, transformation: Union[str, SampleTransform]) -> 'ShardListDataset[T]': ...
    def dsdesc(self) -> Dict[str, Any]: ...
    def _index_to_shard_index(self, idx: int) -> Tuple[int, int]: ...
    def get_shard(self, idx: int) -> Tuple[IndexedTarSamples, int, int]: ...
    def __len__(self) -> int: ...
    def __getitem__(self, idx: int) -> T: ...

class ShardedSampler:
    dataset: ShardListDataset
    chunk_size: int
    shuffle: bool
    drop_last: bool
    
    def __init__(
        self,
        dataset: ShardListDataset,
        chunk_size: int = 10000,
        shuffle: bool = False,
        drop_last: bool = False,
    ) -> None: ...
    
    def __iter__(self) -> Iterator[int]: ...
    def __len__(self) -> int: ...

class ChunkedSampler:
    dataset: ShardListDataset
    chunk_size: int
    shuffle: bool
    drop_last: bool
    
    def __init__(
        self,
        dataset: ShardListDataset,
        chunk_size: int = 10000,
        shuffle: bool = False,
        drop_last: bool = False,
    ) -> None: ...
    
    def __iter__(self) -> Iterator[int]: ...
    def __len__(self) -> int: ...

def DistributedChunkedSampler(
    dataset: ShardListDataset,
    num_replicas: Optional[int] = None,
    rank: Optional[int] = None,
    chunk_size: int = 10000,
    shuffle: bool = True,
    seed: int = 0,
    drop_last: bool = False,
) -> ChunkedSampler: ...