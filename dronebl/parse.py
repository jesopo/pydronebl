from typing    import List, Optional, Tuple
from xml.etree import ElementTree as et
from .struct   import Lookup

def _xml(s: bytes) -> List[et.Element]:
    return list(et.fromstring(s.strip()))

def add(data: bytes) -> List[Tuple[Optional[int], str]]:
    responses = _xml(data)
    out: List[Tuple[Optional[int], str]] = []

    for response in responses:
        id: Optional[int] = None
        if response.tag == "success":
            id = int(response.get("id", ""))
        out.append((id, response.get("data", "")))
    return out

def lookup(data: bytes) -> List[Lookup]:
    responses = _xml(data)
    lookups: List[Lookup] = []
    for response in responses:
        port   = response.get("port", "")
        lookup = Lookup(
            response.get("ip", ""),
            int(response.get("id", "")),
            int(response.get("type", "")),
            response.get("comment", ""),
            None if port == "" else int(port),
            int(response.get("timestamp", ""))
        )
        lookups.append(lookup)
    return lookups

def remove(data: bytes) -> Tuple[bool, str]:
    responses = _xml(data)
    return (
        responses[0].tag == "success",
        responses[0].get("data", "")
    )
