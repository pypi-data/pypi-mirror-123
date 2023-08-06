from .enums import uSwidGlobalMap as uSwidGlobalMap, uSwidRole as uSwidRole
from .errors import NotSupportedError as NotSupportedError
from typing import Any, List, Optional

class uSwidEntity:
    name: Any
    regid: Any
    roles: Any
    def __init__(self, name: Optional[str] = ..., regid: Optional[str] = ..., roles: Optional[List[uSwidRole]] = ...) -> None: ...
