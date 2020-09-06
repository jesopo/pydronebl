import unittest
from binascii  import hexlify
from uuid      import uuid4
from xml.etree import ElementTree as et

from dronebl import make

IP = "198.51.100.123"
ID = 3174874

def _xml(s: str) -> et.Element:
    return et.fromstring(s)

class MakeTestRequest(unittest.TestCase):
    def test(self):
        key  = uuid4().hex
        meth = b"<method />"
        out  = make.request(key.encode("utf8"), meth)
        xml  = _xml(out)

        self.assertEqual(xml.tag,        "request")
        self.assertEqual(xml.get("key"), key)
        kids = list(xml)
        self.assertEqual(len(kids),      1)
        self.assertEqual(kids[0].tag,    "method")

class MakeTestAdd(unittest.TestCase):
    def test_with_port(self):
        out = make.add(IP, 19, "abused vpn", 1337)
        xml = _xml(out)

        self.assertEqual(xml.tag,            "add")
        self.assertEqual(xml.get("ip"),      IP)
        self.assertEqual(xml.get("port"),    "1337")
        self.assertEqual(xml.get("type"),    "19")
        self.assertEqual(xml.get("comment"), "abused vpn")

    def test_without_port(self):
        out = make.add(IP, 19, "abused vpn")
        xml = _xml(out)

        self.assertEqual(xml.tag,            "add")
        self.assertEqual(xml.get("ip"),      IP)
        self.assertEqual(xml.get("port"),    None)
        self.assertEqual(xml.get("type"),    "19")
        self.assertEqual(xml.get("comment"), "abused vpn")

class MakeTestUpdate(unittest.TestCase):
    def test(self):
        out = make.update(ID, "abused vpn")
        xml = _xml(out)

        self.assertEqual(xml.tag,            "update")
        self.assertEqual(xml.get("id"),      str(ID))
        self.assertEqual(xml.get("comment"), "abused vpn")

class MakeTestLookup(unittest.TestCase):
    def test_ip_with_type(self):
        out = make.lookup(IP, 19)
        xml = _xml(out)

        self.assertEqual(xml.tag,                "lookup")
        self.assertEqual(xml.get("ip"),          IP)
        self.assertEqual(xml.get("type"),        "19")
        self.assertEqual(xml.get("listed"),      "1")
        self.assertEqual(xml.get("own", "0"),    "0")
        self.assertEqual(xml.get("limit", None), None)

    def test_ip_without_type(self):
        out = make.lookup(IP)
        xml = _xml(out)

        self.assertEqual(xml.get("type"), None)

    def test_id(self):
        out = make.lookup(ID, 19)
        xml = _xml(out)

        self.assertEqual(xml.get("id"),       str(ID))
        self.assertEqual(xml.get("ip", None), None)

    def test_limit(self):
        out = make.lookup(IP, limit=1337)
        xml = _xml(out)

        self.assertEqual(xml.get("limit"), "1337")

class MakeTestRemove(unittest.TestCase):
    def test(self):
        out = make.remove(ID)
        xml = _xml(out)

        self.assertEqual(xml.tag,       "remove")
        self.assertEqual(xml.get("id"), str(ID))

class MakeTestBatch(unittest.TestCase):
    def test(self):
        bat  = make.Batch()

        bat.add(IP, 19, "abused vpn", 1337)
        ref  = make.add(IP, 19, "abused vpn", 1337)

        bat.remove(ID)
        ref += make.remove(ID)

        acts = [("add", IP), ("remove", str(ID))]

        self.assertEqual(bat.data,    ref)
        self.assertEqual(bat.actions, acts)

    def test_type(self):
        bat = make.TypeBatch(19)
        bat.add(IP, "abused vpn", 1337)
        ref = make.add(IP, 19, "abused vpn", 1337)

        self.assertEqual(bat.data,    ref)
        self.assertEqual(bat.actions, [("add", IP)])
