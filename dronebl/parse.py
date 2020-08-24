from typing    import List, Optional, Tuple
from xml.etree import ElementTree as et
from .struct   import Lookup

def _xml(s: bytes) -> List[et.Element]:
    return list(et.fromstring(s.strip()))

def add(data: bytes) -> Tuple[Optional[int], str]:
    responses = _xml(data)
    id: Optional[int] = None
    if responses[0].tag == "success":
        id = int(responses[0].get("id", ""))
    return (
        id, responses[0].get("data", "")
    )

def lookup(data: bytes) -> Optional[Lookup]:
    responses = _xml(data)
    if (not responses or
            not responses[0].tag == "result"):
        return None
    else:
        response = responses[0]
        port     = response.get("port", "")
        return Lookup(
            response.get("ip", ""),
            int(response.get("id", "")),
            int(response.get("type", "")),
            response.get("comment", ""),
            None if port == "" else int(port),
            int(response.get("timestamp", ""))
        )

def remove(data: bytes) -> Tuple[bool, str]:
    responses = _xml(data)
    return (
        responses[0].tag == "success",
        responses[0].get("data", "")
    )
