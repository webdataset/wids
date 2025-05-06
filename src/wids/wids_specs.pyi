from io import IOBase
from typing import Any, Dict, List, Optional, Union, overload

# Type aliases
URL = str
ShardDict = Dict[str, Any]
ShardList = List[ShardDict]
DatasetDesc = Dict[str, Any]
OptionsDict = Dict[str, Any]

def urldir(url: URL) -> URL: ...

def urlmerge(base: URL, url: URL) -> URL: ...

def check_shards(l: ShardList) -> ShardList: ...

def set_all(l: ShardList, k: str, v: Any) -> None: ...

def load_remote_dsdesc_raw(source: Union[URL, IOBase]) -> DatasetDesc: ...

def rebase_shardlist(shardlist: ShardList, base: Optional[URL]) -> ShardList: ...

def resolve_dsdesc(
    dsdesc: DatasetDesc, 
    *, 
    options: Optional[OptionsDict] = None, 
    base: Optional[URL] = None
) -> ShardList: ...

def load_dsdesc_and_resolve(
    source: Union[URL, IOBase, ShardList, DatasetDesc], 
    *, 
    options: Optional[OptionsDict] = None, 
    base: Optional[URL] = None
) -> ShardList: ...