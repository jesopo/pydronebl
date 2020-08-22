import urllib.request
from datetime  import datetime
from enum      import Enum
from typing    import List, Optional, Tuple
from xml.etree import ElementTree as et

from httpx     import AsyncClient

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

class BaseDroneBL(object):
    def __init__(self, key: str):
        self._key = key

    def _make_add(self,
            ip:      str,
            type:    int,
            comment: str,
            port:    Optional[int]=None
            ) -> str:
        if port is not None:
            method = M_ADD_PORT
        else:
            method = M_ADD
        return method.format(
            ip=ip, type=type, comment=comment, port=port
        )
    def _parse_add(self,
            responses: List[et.Element]
            ) -> Tuple[bool, str]:
        return (
            responses[0].tag == "success",
            responses[0].get("data", "")
        )

    def _make_lookup(self,
            ip:   str,
            type: Optional[int]=None
            ) -> str:
        if type is not None:
            method = M_LOOKUP_TYPE
        else:
            method = M_LOOKUP
        return method.format(ip=ip, type=type)

    def _parse_lookup(self,
            responses: List[et.Element]
            ) -> Optional[Lookup]:
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

    def _make_remove(self,
            id: int
            ) -> str:
        return M_REMOVE.format(id=id)
    def _parse_remove(self,
            responses: List[et.Element]
            ) -> Tuple[bool, str]:
        return (
            responses[0].tag == "success",
            responses[0].get("data", "")
        )

class DroneBL(BaseDroneBL):
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

    def lookup(self,
            ip:   str,
            type: Optional[int]=None
            ) -> Optional[Lookup]:
        method    = self._make_lookup(ip,type)
        responses = self._post(method)
        return self._parse_lookup(responses)

    def add(self,
            ip:      str,
            type:    int,
            comment: str,
            port:    Optional[int]=None
            ) -> Tuple[bool, str]:
        method    = self._make_add(ip, type, comment, port)
        responses = self._post(method)
        return self._parse_add(responses)

    def remove(self,
            id: int
            ) -> Tuple[bool, str]:
        method    = self._make_remove(id)
        responses = self._post(method)
        return self._parse_remove(responses)

class AsyncDroneBL(BaseDroneBL):
    async def _post(self,
            method: str
            ) -> List[et.Element]:
        data     = ENVELOPE.format(key=self._key, method=method)
        async with AsyncClient() as client:
            response = await client.post(
                URL,
                data    = data.encode("utf8"),
                headers = HEADERS
            )
        decoded  = response.content.decode("utf8")
        elements = et.fromstring(decoded)
        return list(elements)

    async def lookup(self,
            ip:   str,
            type: Optional[int]=None
            ) -> Optional[Lookup]:
        method    = self._make_lookup(ip,type)
        responses = await self._post(method)
        return self._parse_lookup(responses)

    async def add(self,
            ip:      str,
            type:    int,
            comment: str,
            port:    Optional[int]=None
            ) -> Tuple[bool, str]:
        method    = self._make_add(ip, type, comment, port)
        responses = await self._post(method)
        return self._parse_add(responses)

    async def remove(self,
            id: int
            ) -> Tuple[bool, str]:
        method    = self._make_remove(id)
        responses = await self._post(method)
        return self._parse_remove(responses)
