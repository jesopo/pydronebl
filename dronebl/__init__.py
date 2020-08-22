import urllib.request
from datetime  import datetime
from enum      import Enum
from typing    import List, Optional, Tuple
from xml.etree import ElementTree as et

URL = \
    "https://dronebl.org/RPC2"
HEADERS = {
    "Content-Type": "text/xml"
}
ENVELOPE = \
    '<?xml version="1.0"?><request key="{key}">{method}</request>'
M_ADD = \
    '<add ip="{ip}" type="{type}" comment="{comment}" />'
M_ADD_PORT = \
    '<add ip="{ip}" type="{type}" comment="{comment}" port="{port}" />'
M_LOOKUP = \
    '<lookup ip="{ip}" listed="1" limit="1" />'
M_LOOKUP_TYPE = \
    '<lookup ip="{ip}" listed="1" limit="1" type="{type}" />'
M_REMOVE = \
    '<remove id="{id}" />'

class Lookup(object):
    def __init__(self,
            id:      int,
            type:    int,
            comment: str,
            port:    Optional[int],
            ts:      int):
        self.id       = id
        self.type     = type
        self.comment  = comment
        self.port     = port
        self.datetime = datetime.utcfromtimestamp(ts)
    def __repr__(self) -> str:
        pieces: List[str] = []
        pieces.append(f"id={self.id!r}")
        pieces.append(f"type={self.type!r}")
        if self.port is not None:
            pieces.append(f"port={self.port!r}")
        pieces.append(f"datetime={self.datetime.isoformat()}")
        pieces.append(f"comment={self.comment!r}")
        return f"Lookup({', '.join(pieces)})"

class DroneBL(object):
    def __init__(self, key: str):
        self._key = key

    def _post(self,
            method: str
            ) -> List[et.Element]:
        data     = ENVELOPE.format(key=self._key, method=method)
        request  = urllib.request.Request(
            URL, data.encode("utf8"), HEADERS, method="POST"
        )
        response = urllib.request.urlopen(request, timeout=5)
        decoded  = response.read().decode("utf8")
        elements = et.fromstring(decoded)
        return list(elements)

    def add(self,
            ip:      str,
            type:    int,
            comment: str,
            port:    Optional[int]=None
            # return (success, message)
            ) -> Tuple[bool, str]:
        if port is not None:
            method = M_ADD_PORT
        else:
            method = M_ADD

        method_f = method.format(
            ip=ip, type=type, comment=comment, port=port
        )
        response = self._post(method_f)[0]
        return (
            response.tag == "success",
            response.get("data", "")
        )

    def lookup(self,
            ip:   str,
            type: Optional[str]=None
            ) -> Optional[Lookup]:
        if type is not None:
            method = M_LOOKUP_TYPE
        else:
            method = M_LOOKUP

        method_f  = method.format(ip=ip, type=type)
        responses = self._post(method_f)
        if (not responses or
                not responses[0].tag == "result"):
            return None
        else:
            response = responses[0]
            port     = response.get("port", "")
            return Lookup(
                int(response.get("id", "")),
                int(response.get("type", "")),
                response.get("comment", ""),
                None if port == "" else int(port),
                int(response.get("timestamp", ""))
            )

    def remove(self,
            id: int
            ) -> Tuple[bool, str]:
        method_f = M_REMOVE.format(id=id)
        response = self._post(method_f)[0]
        return (
            response.tag == "success",
            response.get("data", "")
        )
