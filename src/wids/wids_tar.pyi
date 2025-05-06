from io import BytesIO, IOBase
import tarfile
from typing import Any, Callable, List, Optional, Tuple, Union, overload
import numpy as np

# Type aliases
FilePath = str
FileContent = BytesIO
IndexFileName = str
IndexFinder = Callable[[FilePath], IndexFileName]

def find_index_file(file: FilePath) -> IndexFileName: ...

class TarFileReader:
    verbose: bool
    index_file: Optional[IndexFileName]
    tar_file: tarfile.TarFile
    fnames: List[str]
    index: Union[List[List[int]], np.ndarray]
    
    def __init__(
        self, 
        file: Union[FilePath, IOBase], 
        index_file: Union[IndexFileName, IndexFinder] = find_index_file, 
        verbose: bool = True
    ) -> None: ...
    
    def _create_tar_index(self) -> None: ...
    def names(self) -> List[str]: ...
    def __len__(self) -> int: ...
    def get_file(self, i: int) -> Tuple[str, FileContent]: ...
    def close(self) -> None: ...