# Pyben

Small library for encoding/decoding bencode data.
Pyben Enables fast and easy encoding and decoding of bencoded data.

![PyBen][./assets/pyben.png]

![GitHub repo size](https://img.shields.io/github/repo-size/alexpdev/pyben)
![GitHub contributors](https://img.shields.io/github/license/alexpdev/pyben)
![GitHub stars](https://img.shields.io/badge/rating-99-green)

## Prerequisites

* Python3 installed and enabled

## Installing PyBen

To install PyBen, follow these steps:

Using pip:

```bash
pip install pyben
```

Using git:

```cmd
git clone https://github.com/alexpdev/pyben.git
```

## Using PyBen

The API is intentionally designed to mimic Python's json module.

```python
>>> fd = "path/to/file"
>>> data = {"item1": ["item2", 3, [4], {5: "item6"}]}
>>> encoded = pyben.dumps(data)
>>> encoded
b'd5:item1l5:item2i3eli4eedi5e5:item6eee'
>>> decoded = pybem.loads(encoded)
{'item1': ['item2', 3, [4], {5: 'item6'}]}
```

One key difference is that the 'load' and 'dump' methods accept as arguments,
string paths or path objects as well as open iobuffer.

For Example this:

```python
>> with open("encoded.file", "wb") as fd:
...    pyben.dump(data, fd)
>> with open("encoded.file", "rb") as fd:
...    decoded = pyben.load(fd)
```

is the same as doing following.

```python
>>> pyben.dump(data, "encoded.file")
>>> decoded = pyben.load("encoded.file")
```

The full API includes many other functions and classes as well.
See docs for more full API.

## License

This project uses the following license: GNU LGPL v3
