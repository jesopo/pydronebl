# pydronebl

## usage

The RPC key, IP and ID below are fake.

### looking up an IP

```
>>> from dronebl import DroneBL
>>> d = DroneBL("04efa460cf244b6e88d9d2b8c31eb953")
>>> r = d.lookup("198.51.100.123")
>>> r
Lookup(id=3174874, datetime=2020-08-21T10:18:44, comment='abused VPN (connect verified)')
```

### adding an IP
```
>>> d.add("198.51.100.123", 19, "abused VPN (connect verified)")
(True, 'Added 198.51.100.123')
>>> d.add("198.51.100.123", 19, "abused VPN (connect verified)")
(False, 'You already reported 198.51.100.123 as type 19')
```

### removing an IP
```
>>> d.remove(3174874)
(True, 'Removed 3174874')
>>> d.remove(3174874)
(False, '3174874 already delisted')
```

## contact

Come say hi at [##jess on freenode](https://webchat.freenode.net/?channels=%23%23jess)
