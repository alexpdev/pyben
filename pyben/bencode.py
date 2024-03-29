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
API helper functions for decoding and encoding data with bencode format.

Functions
---------
* bendecode
* bendecode_dict
* bendecode_int
* bendecode_list
* bendecode_str

* benencode
* bencode_bytes
* bencode_dict
* bencode_int
* bencode_list
* bencode_str
"""

import re

from pyben.exceptions import DecodeError, EncodeError


def bendecode(bits: bytes) -> tuple:
    """
    Decode bencoded data.

    Parameters
    ----------
    bits : bytes
        Bencode encoded data.

    Raises
    ------
    DecodeError
        Malformed data.

    Returns
    -------
    tuple
        Bencode decoded data.
    """
    if bits.startswith(b"i"):
        match, feed = bendecode_int(bits)
        return match, feed

    if chr(bits[0]).isdigit():
        match, feed = bendecode_str(bits)
        return match, feed

    if bits.startswith(b"l"):
        lst, feed = bendecode_list(bits)
        return lst, feed

    if bits.startswith(b"d"):
        dic, feed = bendecode_dict(bits)
        return dic, feed

    raise DecodeError(bits)


def bendecode_str(units: bytes) -> str:
    """
    Bendecode string types.

    Parameters
    ----------
    units : bytes
        Bencoded string.

    Returns
    -------
    str
        Decoded data string.

    """
    match = re.match(rb"(\d+):", units)
    word_len, start = int(match.groups()[0]), match.span()[1]
    end = start + word_len
    text = units[start:end]

    try:
        text = text.decode("utf-8")

    except UnicodeDecodeError:
        pass

    return text, end


def bendecode_int(bits: bytes) -> int:
    """
    Decode digits.

    Parameters
    ----------
    bits : bytes
        Bencoded intiger bytes

    Returns
    -------
    int :
        Decoded int value.
    """
    obj = re.match(rb"i(-?\d+)e", bits)
    return int(obj.group(1)), obj.end()


def bendecode_dict(bits: bytes) -> tuple:
    """
    Decode dictionary and it's contents.

    Parameters
    ----------
    bits : bytes
        Bencoded dictionary.

    Returns
    -------
    tuple
        Decoded dictionary and contents
    """
    dic, feed = {}, 1

    while not bits[feed:].startswith(b"e"):
        match1, rest = bendecode(bits[feed:])
        feed += rest
        match2, rest = bendecode(bits[feed:])
        feed += rest
        dic[match1] = match2

    feed += 1
    return dic, feed


def bendecode_list(bits: bytes) -> tuple:
    """
    Decode list and list contents.

    Parameters
    ----------
    bits : bytes
        Bencoded list.

    Returns
    -------
    tuple
        Bencode decoded list and contents.
    """
    lst, feed = [], 1

    while not bits[feed:].startswith(b"e"):
        match, rest = bendecode(bits[feed:])
        lst.append(match)
        feed += rest

    feed += 1
    return lst, feed


def benencode(val) -> bytes:
    """
    Encode data with bencoding.

    Parameters
    ----------
    val : any
        Data for encoding.

    Raises
    ------
    EncodeError
        Cannot interpret data.

    Returns
    -------
    bytes
        Bencoded data.
    """
    if isinstance(val, str):
        return bencode_str(val)

    if isinstance(val, int):
        return bencode_int(val)

    if isinstance(val, list):
        return bencode_list(val)

    if isinstance(val, dict):
        return bencode_dict(val)

    if hasattr(val, "hex"):
        return bencode_bytes(val)

    if isinstance(val, tuple):
        return bencode_list(list(val))

    raise EncodeError(val)


def bencode_bytes(bits: bytes) -> bytes:
    """
    Encode bytes.

    Parameters
    ----------
    bits : bytes
        Bytes treated as a byte-string literal.

    Returns
    -------
    bytes
        Bencode encoded byte string literal.
    """
    size = str(len(bits)) + ":"
    return size.encode("utf-8") + bits


def bencode_str(txt: str) -> bytes:
    """
    Encode string literals.

    Parameters
    ----------
    txt : str
        Any text string.

    Returns
    -------
    bytes
        Bencoded string literal.
    """
    text = txt.encode("utf-8")
    size = str(len(text)) + ":"
    return size.encode("utf-8") + text


def bencode_int(i: int) -> bytes:
    """
    Encode integer type.

    Parameters
    ----------
    i : int
        Number that needs encoding.

    Returns
    -------
    bytes
        Bencoded Integer.
    """
    return ("i" + str(i) + "e").encode("utf-8")


def bencode_list(elems: list) -> bytes:
    """
    Encode list and contents.

    Parameters
    ----------
    elems : list
        List of items for bencoding.

    Returns
    -------
    bytes
        Bencoded list and contents.
    """
    arr = bytearray("l", encoding="utf-8")

    for elem in elems:
        encoded = benencode(elem)
        arr.extend(encoded)

    arr.extend(b"e")
    return arr


def bencode_dict(dic: dict) -> bytes:
    """
    Encode dictionary and contents.

    Parameters
    ----------
    dic : dict
        Any dictionary containing items that can be bencoded.

    Returns
    -------
    bytes :
        Bencoded key, value pairs of data.
    """
    result = b"d"

    for key, val in dic.items():
        result += b"".join([benencode(key), benencode(val)])

    return result + b"e"
