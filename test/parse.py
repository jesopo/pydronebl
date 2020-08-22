import unittest
from base64    import b64encode
from datetime  import datetime
from os        import urandom

from dronebl import parse

IP = "198.51.100.123"
ID = 3174874

def _rand(i: int=16) -> str:
    return b64encode(urandom(i)).decode("ascii")

class ParseTestLookup(unittest.TestCase):
    def test_not_found(self):
        out = parse.lookup( """
            <?xml version="1.0"?>
            <response type="success" />
        """)
        self.assertIsNone(out)

    def test_found(self):
        now  = datetime.utcnow().replace(microsecond=0)
        ts   = int(now.timestamp())
        data = _rand()
        out  = parse.lookup(f"""
            <?xml version="1.0"?>
            <response type="success">
                <result ip="{IP}" type="19" comment="{data}" id="{ID}" listed="1" timestamp="{ts}" />
            </response>
        """)

        self.assertEqual(out.id,       ID)
        self.assertEqual(out.type,     19)
        self.assertEqual(out.comment,  data)
        self.assertEqual(out.datetime, now)

class ParseTestAdd(unittest.TestCase):
    def test_success(self):
        data = _rand()
        out  = parse.add(f"""
            <?xml version="1.0"?>
            <response type="success">
                <success ip="{IP}" id="{ID}" data="{data}" />
            </response>
        """)

        self.assertEqual(out, (ID, data))

    def test_failure(self):
        data = _rand()
        out  = parse.add(f"""
            <?xml version="1.0"?>
            <response type="success">
                <warning ip="{IP}" data="{data}" />
            </response>
        """)

        self.assertEqual(out, (None, data))

class ParseTestRemove(unittest.TestCase):
    def test_success(self):
        data = _rand()
        out  = parse.remove(f"""
            <?xml version="1.0"?>
            <response type="success">
                <success id="{ID}" data="{data}" />
            </response>
        """)

        self.assertEqual(out, (True, data))

    def test_failure(self):
        data = _rand()
        out  = parse.remove(f"""
            <?xml version="1.0"?>
            <response type="success">
                <warning id="{ID}" data="{data}" />
            </response>
        """)

        self.assertEqual(out, (False, data))

