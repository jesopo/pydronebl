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
            method: bytes
            ) -> bytes:
        data     = make.request(self._key, method)
        request  = urllib.request.Request(URL, data, HEADERS, method="POST")
        response = urllib.request.urlopen(request, timeout=5)
        return response.read()

    def lookup(self,
            query: Union[str, int],
            type:  Optional[int]=None,
            limit: Optional[int]=None
            ) -> List[Lookup]:
        method    = make.lookup(query, type, limit)
        responses = self._post(method)
        return parse.lookup(responses)

    def add_many(self,
            ips:     List[str],
            type:    int,
            comment: str,
            port:    Optional[int]=None
            ) -> List[Tuple[Optional[int], str]]:
        method    = make.add(ips, type, comment, port)
        responses = self._post(method)
        return parse.add(responses)
    def add(self,
            ip:      str,
            type:    int,
            comment: str,
            port:    Optional[int]=None
            ) -> Tuple[Optional[int], str]:
        return self.add_many([ip], type, comment, port)[0]

    def remove(self,
            id: int
            ) -> Tuple[bool, str]:
        method    = make.remove(id)
        responses = self._post(method)
        return parse.remove(responses)

class AsyncDroneBL(BaseDroneBL):
    async def _post(self,
            method: bytes
            ) -> bytes:
        data = make.request(self._key, method)
        async with AsyncClient() as client:
            response = await client.post(
                URL, data=data, headers=HEADERS, timeout=5
            )
        return response.content

    async def lookup(self,
            query: Union[str, int],
            type:  Optional[int]=None,
            limit: Optional[int]=None
            ) -> List[Lookup]:
        method    = make.lookup(query, type, limit)
        responses = await self._post(method)
        return parse.lookup(responses)

    async def add_many(self,
            ips:     List[str],
            type:    int,
            comment: str,
            port:    Optional[int]=None
            ) -> List[Tuple[Optional[int], str]]:
        method    = make.add(ips, type, comment, port)
        responses = await self._post(method)
        return parse.add(responses)
    async def add(self,
            ip:      str,
            type:    int,
            comment: str,
            port:    Optional[int]=None
            ) -> Tuple[Optional[int], str]:
        return (await self.add_many([ip], type, comment, port))[0]

    async def remove(self,
            id: int
            ) -> Tuple[bool, str]:
        method    = make.remove(id)
        responses = await self._post(method)
        return parse.remove(responses)
