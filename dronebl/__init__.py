import urllib.request
from typing    import List, Optional, Tuple, Union

from httpx     import AsyncClient

from .         import make, parse
from .struct   import Lookup

URL     = "https://dronebl.org/RPC2"
HEADERS = {"Content-Type": "text/xml"}

class BaseDroneBL(object):
    def __init__(self,
            key:     str,
            timeout: float = 10.0,
            xmlrpc2: str   = URL):
        self._key     = key.encode("ascii")
        self._timeout = timeout
        self._xmlrpc2 = xmlrpc2

    def batch(self) -> make.Batch:
        return make.Batch()
    def type_batch(self, type: int) -> make.TypeBatch:
        return make.TypeBatch(type)

class DroneBL(BaseDroneBL):
    def _post(self,
            method: bytes
            ) -> bytes:
        data     = make.request(self._key, method)
        request  = urllib.request.Request(
            self._xmlrpc2,
            data,
            HEADERS,
            method="POST"
        )
        response = urllib.request.urlopen(request, timeout=self._timeout)
        return response.read()

    def lookup(self,
            query:  Union[str, int],
            type:   Optional[int]=None,
            limit:  Optional[int]=None,
            listed: Optional[int]=2
            ) -> List[Lookup]:
        method    = make.lookup(query, type, limit, listed)
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

    def update(self,
            id:      int,
            comment: str
            ) -> Tuple[bool, str]:
        method    = make.update(id, comment)
        responses = self._post(method)
        return parse.update(responses)

    def remove(self,
            id: int
            ) -> Tuple[bool, str]:
        method    = make.remove(id)
        responses = self._post(method)
        return parse.remove(responses)

    def commit(self,
            batch: make.Batch
            ) -> List[Tuple[str, Union[bool, Optional[int]], str]]:
        if batch.data:
            responses = self._post(batch.data)
            return parse.batch(responses, batch.actions)
        else:
            return []

class AsyncDroneBL(BaseDroneBL):
    async def _post(self,
            method: bytes
            ) -> bytes:
        data = make.request(self._key, method)
        async with AsyncClient() as client:
            response = await client.post(
                self._xmlrpc2,
                data=data,
                headers=HEADERS,
                timeout=self._timeout
            )
        return response.content

    async def lookup(self,
            query:  Union[str, int],
            type:   Optional[int]=None,
            limit:  Optional[int]=None,
            listed: Optional[int]=None
            ) -> List[Lookup]:
        method    = make.lookup(query, type, limit, listed)
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

    async def update(self,
            id:      int,
            comment: str
            ) -> Tuple[bool, str]:
        method    = make.update(id, comment)
        responses = await self._post(method)
        return parse.update(responses)

    async def remove(self,
            id: int
            ) -> Tuple[bool, str]:
        method    = make.remove(id)
        responses = await self._post(method)
        return parse.remove(responses)

    async def commit(self,
            batch: make.Batch
            ) -> List[Tuple[str, Union[bool, Optional[int]], str]]:
        if batch.data:
            responses = await self._post(batch.data)
            return parse.batch(responses, batch.actions)
        else:
            return []
