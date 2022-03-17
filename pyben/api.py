#! /usr/bin/python3
# -*- coding: utf-8 -*-

#####################################################################
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#####################################################################
"""
# Bencode utility library.

Features simple API inspired by json and pickle modules in stdlib.

Functions
---------
* dump
* dumps
* load
* loads
* tojson

## Usage Examples

### Encode inline code:

    >>> import os
    >>> import pyben
    >>> data = {"item1": ["item2", 3, [4], {5: "item6"}]}
    >>> encoded = pyben.dumps(data)
    >>> encoded
    ... b'd5:item1l5:item2i3eli4eedi5e5:item6eee'

### Encode to file:

    >>> fd = "path/to/file"
    >>> pyben.dump(data, fd)
    >>> os.path.exists(fd)
    ... True
    >>> encoded_file = open(fd, "rb").read()
    >>> encoded_file == encoded
    ... True

### Decode inline code:

    >>> decoded = pybem.loads(encoded)
    >>> decoded
    ... {'item1': ['item2', 3, [4], {5: 'item6'}]}
    >>> decoded == data
    ... True

### Decode from file:

    >>> decoded_file = pyben.load(fd)
    >>> decoded_file
    ... {'item1': ['item2', 3, [4], {5: 'item6'}]}
    >>> decoded_file == data
    ... True

"""

from pyben.bencode import bendecode, benencode
from pyben.exceptions import FilePathError


def dump(obj, buffer):
    """
    Shortcut function for bencode encode data and write to file.

    Works effectively the same as it's json equivelant except also
    accepts a path as well as an open fileIO.

    Parameters
    ----------
    obj : any
        Data to be encoded.
    buffer : `str` or `BytesIO`
        File of path-like to write the data to.

    """
    encoded = benencode(obj)

    if not hasattr(buffer, "write"):
        if hasattr(buffer, "decode"):  # pragma: nocover
            txt = buffer.decode("utf-8")
        else:
            txt = buffer
        with open(txt, "wb") as _fd:
            _fd.write(encoded)
    else:
        buffer.write(encoded)


def dumps(obj):
    """
    Shortuct function to encoding given obj to bencode encoding.

    Parameters
    ----------
    obj : `any`
        Object to be encoded.py.

    Returns
    -------
    `bytes` :
        Encoded data.

    """
    return bytes(benencode(obj))


def load(buffer, to_json=False):
    """
    Load bencoded data from a file of path object and decodes it.

    Parameters
    ----------
    buffer : `str` or `BytesIO`
        Open and/or read data from file to be decoded.
    to_json : `bool`
        convert to json serializable metadata if True else leave it alone.

    Returns
    -------
    `any` :
        (commonly `dict`), Decoded contents of file.

    """
    if buffer in [None, ""]:
        raise FilePathError(buffer)

    if hasattr(buffer, "read"):
        decoded, _ = bendecode(buffer.read())
    else:
        if hasattr(buffer, "decode"):  # pragma: nocover
            path = buffer.decode("utf-8")
        else:
            path = buffer
        try:
            with open(path, "rb") as _fd:
                decoded, _ = bendecode(_fd.read())
        except FileNotFoundError as e:
            raise FilePathError(buffer) from e
    if to_json:
        decoded = _to_json(decoded)
    return decoded


def loads(encoded, to_json=False):
    """
    Shortcut function for decoding encoded data.

    Parameters
    ----------
    encoded : `bytes`
        Bencoded data.
    to_json : `bool`
        Convert to json serializable if true otherwise leave it alone.

    Returns
    -------
    any :
        (any), Decoded data.

    """
    decoded, _ = bendecode(encoded)
    if to_json:
        decoded = _to_json(decoded)
    return decoded


def _to_json(decoded):
    """
    Convert bencode decoded output into json serializable object.

    Parameters
    ----------
    decoded : `any`
        decoded input data with unknown data type.

    Returns
    -------
    `dict` :
        json serializable dictionary.
    """
    if isinstance(decoded, (bytes, bytearray)):
        return decoded.hex()
    if isinstance(decoded, (str, int, float)):
        return decoded
    if isinstance(decoded, (list, tuple)):
        seq = []
        for item in decoded:
            seq.append(_to_json(item))
        return seq
    pairs = {}
    if isinstance(decoded, dict):
        for key, val in decoded.items():
            dekey = _to_json(key)
            pairs[dekey] = _to_json(val)
    return pairs


def show(inp):
    """
    Ouptut readable metadata.

    Parameters
    ----------
    inp : any
        Pre-formatted input type.

    Returns
    -------
    bool :
        Returns True if completed successfully.
    """
    import json
    import os
    import sys

    if isinstance(inp, dict):
        meta = _to_json(inp)
    elif hasattr(inp, "read"):
        meta = load(inp, to_json=True)

    elif isinstance(inp, (str, os.PathLike)):
        try:
            meta = load(inp, to_json=True)
        except FilePathError:
            meta = inp
    elif isinstance(inp, (bytes, bytearray)):
        meta = loads(inp, to_json=True)

    json.dump(meta, sys.stdout, indent=4)
    return True
