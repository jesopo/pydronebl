from typing    import Optional, Union
from xml.etree import ElementTree as et

ENVELOPE = b'<?xml version="1.0"?><request key="%b">%b</request>'

def request(
        key:    str,
        method: bytes
        ) -> bytes:
    return ENVELOPE % (key, method)

def lookup(
        query: Union[str, int],
        type:  Optional[int]=None,
        limit: Optional[int]=None
        ) -> bytes:
    # 1000 is default, as per docs
    limit_n = 1000
    if limit is not None:
        limit_n = limit

    element = et.Element("lookup", {
        "limit":  str(limit),
        "listed": "1"
    })

    if isinstance(query, int):
        element.set("id", str(query))
    else:
        element.set("ip", query)

    if type is not None:
        element.set("type", str(type))
    return et.tostring(element)

def add(
        ip:      str,
        type:    int,
        comment: str,
        port:    Optional[int]=None
        ) -> bytes:
    element = et.Element("add", {
        "ip":      ip,
        "type":    str(type),
        "comment": comment
    });
    if port is not None:
        element.set("port", str(port))
    return et.tostring(element)

def remove(id: int) -> bytes:
    element = et.Element("remove", {
        "id": str(id)
    })
    return et.tostring(element)
