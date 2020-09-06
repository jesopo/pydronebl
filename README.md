# pydronebl

[![Build Status](https://travis-ci.org/jesopo/pydronebl.svg?branch=master)](https://travis-ci.org/jesopo/pydronebl)

## Installation

```
$ pip3 install dronebl
```

## Usage

The RPC key, IP and ID below are fake.

### Looking up an IP

returns `None` if not found
```python
>>> from dronebl import DroneBL
>>> d = DroneBL("04efa460cf244b6e88d9d2b8c31eb953")
>>> # by IP
>>> d.lookup("198.51.100.123")
Lookup(198.51.100.123, id=3174874, type=19, datetime=2020-08-21T10:18:44, comment='abused VPN (connect verified)')
>>> # by ID
>>> d.lookup(3174874)
Lookup(198.51.100.123, id=3174874, type=19, datetime=2020-08-21T10:18:44, comment='abused VPN (connect verified)')
```

### Adding an IP
```python
>>> d.add("198.51.100.123", 19, "abused VPN (connect verified)")
(3174874, 'Added 198.51.100.123')
>>> d.add("198.51.100.123", 19, "abused VPN (connect verified)")
(None, 'You already reported 198.51.100.123 as type 19')
```

### Adding with a port
```python
>>> d.add("198.51.100.123", 19, "abused VPN (connect verified)", 1337)
(3174874, 'Added 198.51.100.123')
```

### Adding multiple IPs
```python
>>> d.add(["198.51.100.123", "198.51.100.124"], 19, "abused VPN (connect verified)")
[(3174874, 'Added 198.51.100.123'), (3174875, 'Added 198.51.100.124')]
```

### Removing an IP
```python
>>> d.remove(3174874)
(True, 'Removed 3174874')
>>> d.remove(3174874)
(False, '3174874 already delisted')
```

### Asyncified!

identical methods are offered on the async version of `DroneBL`, `AsyncDroneBL`

```python
>>> from dronebl import AsyncDroneBL
>>> d = AsyncDroneBL("04efa460cf244b6e88d9d2b8c31eb953")
>>> await d.lookup("198.51.100.123")
Lookup(198.51.100.123, id=3174874, type=19, datetime=2020-08-21T10:18:44, comment='abused VPN (connect verified)')
```

## Contact

Come say hi at [##jess on freenode](https://webchat.freenode.net/?channels=%23%23jess)
