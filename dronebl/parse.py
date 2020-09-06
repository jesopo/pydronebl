from typing    import List, Optional, Tuple, Union
from xml.etree import ElementTree as et
from .struct   import Lookup

def _xml(s: bytes) -> List[et.Element]:
    return list(et.fromstring(s.strip()))

def _add(response: et.Element) -> Tuple[Optional[int], str]:
    id: Optional[int] = None
    if response.tag == "success":
        id = int(response.get("id", ""))
    return (id, response.get("data", ""))
def add(data: bytes) -> Tuple[Optional[int], str]:
    responses = _xml(data)
    return _add(responses[0])

def lookup(data: bytes) -> List[Lookup]:
    responses = _xml(data)
    lookups: List[Lookup] = []
    for response in responses:
        if response.tag == "result":
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

def _remove(response: et.Element) -> Tuple[bool, str]:
    return (
        response.tag == "success",
        response.get("data", "")
    )
def remove(data: bytes) -> Tuple[bool, str]:
    responses = _xml(data)
    return _remove(responses[0])

def batch(
        data:    bytes,
        actions: List[Tuple[str, Union[str, int]]]
        ) -> List[Tuple[str, Union[bool, Optional[int]], str]]:
    responses = _xml(data)
    outs: List[Tuple[str, Union[bool, Optional[int]], str]] = []

    j = 0
    for i in range(len(responses)):
        action, ident = actions[j]
        response      = responses[i]

        if ((action == "add" and response.get("ip") == ident) or
                (action == "remove" and response.get("id") == ident)):
            j += 1
            if   action == "add":
                id, msg  = _add(response)
                outs.append((action, id,  msg))
            elif action == "remove":
                suc, msg = _remove(response)
                outs.append((action, suc, msg))
    return outs
