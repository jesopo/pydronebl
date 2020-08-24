import unittest
from xml.etree import ElementTree as et

from dronebl import make

IP = "198.51.100.123"
ID = 3174874

def _xml(s: str) -> et.Element:
    return et.fromstring(s)

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

class MakeTestLookup(unittest.TestCase):
    def test_ip_with_type(self):
        out = make.lookup(IP, 19)
        xml = _xml(out)

        self.assertEqual(xml.tag,             "lookup")
        self.assertEqual(xml.get("ip"),       IP)
        self.assertEqual(xml.get("type"),     "19")
        self.assertEqual(xml.get("listed"),   "1")
        self.assertEqual(xml.get("own", "0"), "0")

    def test_ip_without_type(self):
        out = make.lookup(IP)
        xml = _xml(out)

        self.assertEqual(xml.tag,             "lookup")
        self.assertEqual(xml.get("ip"),       IP)
        self.assertEqual(xml.get("type"),     None)
        self.assertEqual(xml.get("listed"),   "1")
        self.assertEqual(xml.get("own", "0"), "0")

    def test_id_with_type(self):
        out = make.lookup(ID, 19)
        xml = _xml(out)

        self.assertEqual(xml.tag,             "lookup")
        self.assertEqual(xml.get("id"),       str(ID))
        self.assertEqual(xml.get("type"),     "19")
        self.assertEqual(xml.get("listed"),   "1")
        self.assertEqual(xml.get("own", "0"), "0")


    def test_id_without_type(self):
        out = make.lookup(ID)
        xml = _xml(out)

        self.assertEqual(xml.tag,             "lookup")
        self.assertEqual(xml.get("id"),       str(ID))
        self.assertEqual(xml.get("type"),     None)
        self.assertEqual(xml.get("listed"),   "1")
        self.assertEqual(xml.get("own", "0"), "0")

class MakeTestRemove(unittest.TestCase):
    def test(self):
        out = make.remove(ID)
        xml = _xml(out)

        self.assertEqual(xml.tag,       "remove")
        self.assertEqual(xml.get("id"), str(ID))
