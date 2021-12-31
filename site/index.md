# Pyben

Small library for encoding/decoding bencode data.
Pyben Enables fast and easy encoding and decoding of bencoded data.

![PyBen](./assets/pyben.png)

---------

![GitHub repo size](https://img.shields.io/github/repo-size/alexpdev/pyben&style=flat-square)
![GitHub contributors](https://img.shields.io/github/license/alexpdev/pyben)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyben?color=%23CC3919&label=PyPi%20Downloads&logo=PyPi&logoColor=cyan&style=flat-square)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/af86338dcf0a4a899228df470d20e894)](https://www.codacy.com/gh/alexpdev/pyben/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alexpdev/pyben&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/af86338dcf0a4a899228df470d20e894)](https://www.codacy.com/gh/alexpdev/pyben/dashboard?utm_source=github.com&utm_medium=referral&utm_content=alexpdev/pyben&utm_campaign=Badge_Coverage)
[![codecov](https://codecov.io/gh/alexpdev/pyben/branch/master/graph/badge.svg?token=N6TCUUQ6CJ)](https://codecov.io/gh/alexpdev/pyben)

## Prerequisites

Python v3.6+

## Installing PyBen

To install PyBen, follow these steps:

Using pip:

`pip install pyben`

Using git:

`git clone https://github.com/alexpdev/pyben.git`

## Using PyBen

The API is intentionally designed to mimic Python's json and pickle modules.

    >>> import os
    >>> import pyben
    >>> file_path = "path/to/encoded.file"
    >>> data = {"item1": ["item2", 3, [4], {5: "item6"}]}
    >>> encoded = pyben.dumps(data)
    >>> encoded
    ... b'd5:item1l5:item2i3eli4eedi5e5:item6eee'
    >>> decoded = pyben.loads(encoded)
    >>> decoded
    ... {'item1': ['item2', 3, [4], {5: 'item6'}]}
    >>> decoded == data
    ... True

One key difference is that the 'load' and 'dump' methods accept as arguments,
string paths or path objects as well as open iobuffer.

For Example this:

    >>> with open(file_path, "wb") as fd:
    >>>    pyben.dump(decoded, fd)
    >>> os.path.exists(file_path)
    ... True
    >>> with open(file_path, "rb") as fd:
    >>>    decoded_file = pyben.load(fd)
    >>> decoded_file == decoded == data
    ... True

is the same as doing following.

    >>> pyben.dump(data, file_path)
    >>> os.path.exists(file_path)
    ... True
    >>> decoded_file = pyben.load(file_path)
    >>> decoded_file == decoded == data
    ... True

The full API includes many other functions and classes as well.
See docs for more full API.

## License

This project uses the following license: GNU LGPL v3
