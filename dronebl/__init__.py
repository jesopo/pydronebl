import urllib.request
from typing    import List, Optional, Tuple, Union

from httpx     import AsyncClient

from .         import make, parse
from .struct   import Lookup

URL     = "https://dronebl.org/RPC2"
HEADERS = {"Content-Type": "text/xml"}

class BaseDroneBL(object):
    def __init__(self, key: str):
        self._key = key

class DroneBL(BaseDroneBL):
    def _post(self,
            method: str
            ) -> str:
        data     = make.request(self._key, method)
        request  = urllib.request.Request(
            URL, data.encode("utf8"), HEADERS, method="POST"
        )
        response = urllib.request.urlopen(request, timeout=5)
        return response.read().decode("utf8")

    def lookup(self,
            query: Union[str, int],
            type:  Optional[int]=None
            ) -> Optional[Lookup]:
        method    = make.lookup(query, type)
        responses = self._post(method)
        return parse.lookup(responses)

    def add(self,
            ip:      str,
            type:    int,
            comment: str,
            port:    Optional[int]=None
            ) -> Tuple[Optional[int], str]:
        method    = make.add(ip, type, comment, port)
        responses = self._post(method)
        return parse.add(responses)

    def remove(self,
            id: int
            ) -> Tuple[bool, str]:
        method    = make.remove(id)
        responses = self._post(method)
        return parse.remove(responses)

class AsyncDroneBL(BaseDroneBL):
    async def _post(self,
            method: str
            ) -> str:
        data = make.request(self._key, method)
        async with AsyncClient() as client:
            response = await client.post(
                URL,
                data    = data.encode("utf8"),
                headers = HEADERS
            )
        return response.content.decode("utf8")

    async def lookup(self,
            query: Union[str, int],
            type:  Optional[int]=None
            ) -> Optional[Lookup]:
        method    = make.lookup(query, type)
        responses = await self._post(method)
        return parse.lookup(responses)

    async def add(self,
            ip:      str,
            type:    int,
            comment: str,
            port:    Optional[int]=None
            ) -> Tuple[Optional[int], str]:
        method    = make.add(ip, type, comment, port)
        responses = await self._post(method)
        return parse.add(responses)

    async def remove(self,
            id: int
            ) -> Tuple[bool, str]:
        method    = make.remove(id)
        responses = await self._post(method)
        return parse.remove(responses)
