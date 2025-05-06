from io import BytesIO
from typing import Any, Dict, Optional, Union, overload

# Type aliases
SampleType = Dict[str, Any]
FormatType = Optional[Union[bool, str]]

def check_keys(sample: SampleType) -> None: ...

def decode_all_gz(
    sample: SampleType, 
    format: FormatType = True, 
    update_key: bool = True
) -> SampleType: ...

def decode_basic(sample: SampleType, format: FormatType = True) -> SampleType: ...

def decode_images_to_pil(sample: SampleType, format: FormatType = True) -> SampleType: ...

def decode_images_to_numpy(sample: SampleType, format: FormatType = True) -> SampleType: ...

def default_decoder(
    sample: SampleType,
    format: FormatType = True,
    gz_update_key: bool = False,
) -> SampleType: ...