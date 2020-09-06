from typing    import List, Optional, Union
from xml.etree import ElementTree as et

ENVELOPE = b'<?xml version="1.0"?><request key="%b">%b</request>'

def request(
        key:    bytes,
        method: bytes
        ) -> bytes:
    return ENVELOPE % (key, method)

def lookup(
        query: Union[str, int],
        type:  Optional[int]=None,
        limit: Optional[int]=None
        ) -> bytes:
    element = et.Element("lookup", {
        "listed": "1"
    })

    if isinstance(query, int):
        element.set("id", str(query))
    else:
        element.set("ip", query)

    if type is not None:
        element.set("type", str(type))

    if limit is not None:
        element.set("limit", str(limit))

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

def update(
        id:      int,
        comment: str
        ) -> bytes:
    element = et.Element("update", {
        "id":      str(id),
        "comment": comment
    })
    return et.tostring(element)

def remove(id: int) -> bytes:
    element = et.Element("remove", {
        "id": str(id)
    })
    return et.tostring(element)

class BaseBatch(object):
    def __init__(self):
        self._actions: List[Tuple[str, str]] = []
        self._data = b""

    @property
    def actions(self):
        return self._actions
    @property
    def data(self):
        return self._data

    def remove(self, id: int):
        self._actions.append(("remove", str(id)))
        self._data += remove(id)

    def update(self,
            id:      int,
            comment: str):
        self._actions.append(("update", str(id)))
        self._data += update(id, comment)

class Batch(BaseBatch):
    def add(self,
            ip:      str,
            type:    int,
            comment: str,
            port:    Optional[int]=None):
        self._actions.append(("add", ip))
        self._data += add(ip, type, comment, port)

class TypeBatch(BaseBatch):
    def __init__(self, type: int):
        self._type = type
        super().__init__()

    def add(self,
            ip:      str,
            comment: str,
            port:    Optional[int]=None):
        self._actions.append(("add", ip))
        self._data += add(ip, self._type, comment, port)
