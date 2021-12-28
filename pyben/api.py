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

from .bencode import bendecode, benencode
from .exceptions import FilePathError


def dump(obj, buffer):
    """
    Shortcut function for bencode encode data and write to file.

    Works effectively the same as it's json equivelant except also
    accepts a path as well as an open fileIO.

    Args:
    ----
    obj : any
        Data to be encoded.
    buffer : `str` or `BytesIO`
        File of path-like to write the data to.

    """
    encoded = benencode(obj)

    if not hasattr(buffer, "write"):
        with open(buffer, "wb") as _fd:
            _fd.write(encoded)
    else:
        buffer.write(encoded)


def dumps(obj):
    """
    Shortuct function to encoding given obj to bencode encoding.

    Args
    ----
    obj : `any`
        Object to be encoded.py.

    Returns
    -------
    `bytes` :
        Encoded data.

    """
    return bytes(benencode(obj))


def load(buffer, json=False):
    """
    Load bencoded data from a file of path object and decodes it.

    Args
    ----
    buffer : `str` or `BytesIO`
        Open and/or read data from file to be decoded.

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
        try:
            with open(buffer, "rb") as _fd:
                decoded, _ = bendecode(_fd.read())
        except FileNotFoundError as excp:
            raise FilePathError(buffer) from excp
     
    if json:
        decoded = _to_json(decoded)
        decoded = json.dumps(decoded)
    return decoded


def loads(encoded, json=False):
    """
    Shortcut function for decoding encoded data.

    Args
    ----
    encoded : `bytes`
        Bencoded data.

    Returns
    -------
    any :
        (any), Decoded data.

    """
    decoded, _ = bendecode(encoded)
    if json:
        import json
        decoded = _to_json(decoded)
        decoded = json.dumps(decoded)
        
    return decoded
                

def _to_json(decoded):
    """Convert bencode decoded output into json serializable object."""
    if isinstance(decoded, dict):
        pairs = {}
        for key, val in decoded.items():
            pairs[key] = _to_json(val)
        return pairs
    elif isinstance(decoded, (bytes, bytearray)):
        return decoded.hex()
    elif isinstance(decoded, (str, int, float)):
        return decoded
    elif isinstance(decoded, (list, tuple)):
        seq = []
        for item in decoded:
            seq.append(_to_json(item))
        return seq
    else:
        return decoded
        