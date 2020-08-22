from datetime import datetime
from typing   import List, Optional

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
