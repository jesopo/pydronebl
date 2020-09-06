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
        out = parse.lookup(b"""
            <?xml version="1.0"?>
            <response type="success" />
        """)
        self.assertEqual(out, [])

    def test_found(self):
        now  = datetime.utcnow().replace(microsecond=0)
        ts   = int(now.timestamp())
        data = _rand()
        outs = parse.lookup(f"""
            <?xml version="1.0"?>
            <response type="success">
                <result ip="{IP}" type="19" comment="{data}" id="{ID}" listed="1" timestamp="{ts}" />
            </response>
        """.encode("utf8"))

        self.assertEqual(len(outs),    1)
        out  = outs[0]
        self.assertEqual(out.ip,       IP)
        self.assertEqual(out.id,       ID)
        self.assertEqual(out.type,     19)
        self.assertEqual(out.comment,  data)
        self.assertEqual(out.datetime, now)

    def test_invalid(self):
        outs = parse.lookup(f"""
            <?xml version="1.0"?>
            <response type="success">
                <warning ip="{IP}" data="{IP} is not a valid IPv4/IPv6 address or cidr." />
            </response>
        """.encode("utf8"))
        self.assertEqual(outs, [])

class ParseTestAdd(unittest.TestCase):
    def test_success(self):
        data = _rand()
        out  = parse.add(f"""
            <?xml version="1.0"?>
            <response type="success">
                <success ip="{IP}" id="{ID}" data="{data}" />
            </response>
        """.encode("utf8"))

        self.assertEqual(out, (ID, data))

    def test_failure(self):
        data = _rand()
        out  = parse.add(f"""
            <?xml version="1.0"?>
            <response type="success">
                <warning ip="{IP}" data="{data}" />
            </response>
        """.encode("utf8"))

        self.assertEqual(out, (None, data))

class ParseTestUpdate(unittest.TestCase):
    def test_success(self):
        data = _rand()
        out  = parse.update(f"""
            <?xml version="1.0"?>
            <response type="success">
                <success id="{ID}" data="{data}" />
            </response>
        """.encode("utf8"))
        self.assertEqual(out, (True, data))

    def test_failure(self):
        data = _rand()
        out  = parse.update(f"""
            <?xml version="1.0"?>
            <response type="success">
                <warning id="{ID}" data="{data}" />
            </response>
        """.encode("utf8"))
        self.assertEqual(out, (False, data))

class ParseTestRemove(unittest.TestCase):
    def test_success(self):
        data = _rand()
        out  = parse.remove(f"""
            <?xml version="1.0"?>
            <response type="success">
                <success id="{ID}" data="{data}" />
            </response>
        """.encode("utf8"))

        self.assertEqual(out, (True, data))

    def test_failure(self):
        data = _rand()
        out  = parse.remove(f"""
            <?xml version="1.0"?>
            <response type="success">
                <warning id="{ID}" data="{data}" />
            </response>
        """.encode("utf8"))

        self.assertEqual(out, (False, data))

class ParseTestBatch(unittest.TestCase):
    def test(self):
        data = _rand()
        acts = [("add", IP), ("remove", str(ID))]
        out  = parse.batch(f"""
            <?xml version="1.0"?>
            <response type="success">
                <success ip="{IP}" id="{ID}" data="{data}" />
                <success id="{ID}" data="{data}" />
            </response>
        """.encode("utf8"), acts)

        self.assertEqual(len(out), 2)
        self.assertEqual(out[0],   ("add",    ID, data))
        self.assertEqual(out[1],   ("remove", True, data))

    def test_junk(self):
        data = _rand()
        acts = [("add", IP), ("remove", str(ID))]
        out  = parse.batch(f"""
            <?xml version="1.0"?>
            <response type="success">
                <success ip="{IP}" id="{ID}" data="{data}" />
                <warning />
                <success id="{ID}" data="{data}" />
            </response>
        """.encode("utf8"), acts)

        self.assertEqual(len(out), 2)
        self.assertEqual(out[0],   ("add",    ID, data))
        self.assertEqual(out[1],   ("remove", True, data))
