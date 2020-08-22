from typing import Optional, Union

ENVELOPE = \
    '<?xml version="1.0"?><request key="{key}">{method}</request>'
M_ADD = \
    '<add ip="{ip}" type="{type}" comment="{comment}" />'
M_ADD_PORT = \
    '<add ip="{ip}" type="{type}" comment="{comment}" port="{port}" />'
M_LOOKUP = \
    '<lookup {query_k}="{query_v}" listed="1" limit="1" />'
M_LOOKUP_TYPE = \
    '<lookup {query_k}="{query_v}" listed="1" limit="1" type="{type}" />'
M_REMOVE = \
    '<remove id="{id}" />'

def request(
        key: str,
        method: str
        ) -> str:
    return ENVELOPE.format(key=key, method=method)

def lookup(
        query: Union[str, int],
        type:  Optional[int]=None
        ) -> str:
    if isinstance(query, int):
        query_k = "id"
        query_v = str(query)
    else:
        query_k = "ip"
        query_v = query

    if type is not None:
        method = M_LOOKUP_TYPE
    else:
        method = M_LOOKUP
    return method.format(query_k=query_k, query_v=query_v, type=type)

def add(
        ip:      str,
        type:    int,
        comment: str,
        port:    Optional[int]=None
        ) -> str:

    if port is not None:
        method = M_ADD_PORT
    else:
        method = M_ADD
    return method.format(ip=ip, type=type, comment=comment, port=port)

def remove(id: int) -> str:
    return M_REMOVE.format(id=id)
