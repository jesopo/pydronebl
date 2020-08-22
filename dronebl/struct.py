from datetime import datetime
from typing   import List, Optional

class Lookup(object):
    def __init__(self,
            ip:      str,
            id:      int,
            type:    int,
            comment: str,
            port:    Optional[int],
            ts:      int):
        self.ip       = ip
        self.id       = id
        self.type     = type
        self.comment  = comment
        self.port     = port
        self.datetime = datetime.utcfromtimestamp(ts)

    def __repr__(self) -> str:
        pieces: List[str] = [
            self.ip,
            f"id={self.id!r}",
            f"type={self.type!r}",
            f"datetime={self.datetime.isoformat()}",
            f"comment={self.comment!r}"
        ]
        if self.port is not None:
            pieces.insert(3, f"port={self.port!r}")
        return f"Lookup({', '.join(pieces)})"
