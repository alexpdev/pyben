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

import re
from pyben.exceptions import DecodeError, EncodeError

"""
Library of functions and classes for encoding and decoding bencoded data.

Usage: How to Encode/Decode:

>>> import pyben
>>> fd = "path/to/file"
>>> data = {"item1": ["item2", 3, [4], {5: "item6"}]}
>>> encoded = pyben.dumps(data)
>>> encoded
b'd5:item1l5:item2i3eli4eedi5e5:item6eee'
>>> decoded = pybem.loads(encoded)
{'item1': ['item2', 3, [4], {5: 'item6'}]}

"""

def dump(obj, iobuffer):
    """
    dump(obj, iobuffer)

    Shortcut function for bencode encode data and write to file.

    Args
    -------
    * obj : any
        Data to be encoded.
    * iobuffer : IOBuffer
        File of path-like to write the data to.
    """
    encoded = benencode(obj)
    if hasattr(iobuffer, "write"):
        iobuffer.write(encoded)
        return iobuffer.close()
    else:
        with open(iobuffer, "wb") as fd:
            fd.write(encoded)
    return iobuffer


def dumps(obj):
    """
    dumps(obj)

    Shortuct function to encoding given obj to bencode encoding.

    Args
    --------
    obj : any
        object to be encoded.py

    Returns
    ---------
    bytes:
         encoded data
    """
    return benencode(obj)

def load(iobuffer):
    """
    load(iobuffer)

    Loads bencoded data from a file of path object and decodes it.

    Args
    --------
    iobuffer : path or file
        Open and/or read data from file to be decoded

    Returns
    ---------
    (any)
        usually a dictionary... decoded data
    """
    if hasattr(iobuffer, "read"):
        decoded, _ = bendecode(iobuffer.read())
    else:
        with open(iobuffer, "rb") as fd:
            decoded, _ = bendecode(fd.read())
    return decoded

def loads(encoded):
    """
    loads(encoded)

    Shortcut function for decoding encoded data.py.

    Args
    --------
    encoded : bytes
        Bencoded data.

    Returns
    ---------
    any:
         usually a dictionary, decoded data.
    """
    decoded, _ = bendecode(encoded)
    return decoded


def bendecode_str(bits):
    """
    bendecode_str(bits)

    Bendecode string types.

    Args
    --------
    bits : bytes
        Bencoded string

    Returns
    ---------
    str:
         Decoded data string
    """
    match = re.match(br"(\d+):", bits)
    word_len, start = int(match.groups()[0]), match.span()[1]
    word = bits[start : start + word_len]
    try:
        word = word.decode("utf-8")
    except:
        word = word.hex()
    return word, start + word_len


def bendecode_int(bits):
    """
    bendecode_int

    Decode digits.

    Args
    --------
    bits : bytes
        Bencoded intiger bytes

    Returns
    ---------
    int:
         decoded int value
    """
    obj = re.match(br"i(-?\d+)e", bits)
    return int(obj.group(1)), obj.end()


def bendecode_dict(bits):
    """
    bendecode_dict

    Decode dictionary and it's contents.

    Args
    --------
    bits : bytes
        Bencoded dictionary.

    Returns
    ---------
    dict
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


def bendecode_list(bits):
    """
    bendecode_list

    Decode list and list contents.

    Args
    --------
    bits : bytes
        Bencoded list.

    Returns
    ---------
    list:
         decoded list and contents.
    """
    lst, feed = [], 1
    while not bits[feed:].startswith(b"e"):
        match, rest = bendecode(bits[feed:])
        lst.append(match)
        feed += rest
    feed += 1
    return lst, feed


def bendecode(bits):
    """
    bendecode

    Decode bencoded data.

    Args
    --------
    bits : bytes
        Bencoded data.

    Raises
    --------
    Exception
        Malformed data.

    Returns
    ---------
    any:
         decoded data.
    """
    if bits.startswith(b"i"):
        match, feed = bendecode_int(bits)
        return match, feed
    elif chr(bits[0]).isdigit():
        match, feed = bendecode_str(bits)
        return match, feed
    elif bits.startswith(b"l"):
        lst, feed = bendecode_list(bits)
        return lst, feed
    elif bits.startswith(b"d"):
        dic, feed = bendecode_dict(bits)
        return dic, feed
    else:
        raise DecodeError(bits)


def benencode(val):
    """
    benencode

    Encode data with bencoding.

    Args
    --------
    val : any
        Data for encoding.


    Raises
    --------
    Exception:
        BenencodingError.

    Returns
    ---------
    bytes:
         Bencoded data.
    """
    if type(val) == str:
        return bencode_str(val)
    elif type(val) == int:
        return bencode_int(val)
    elif type(val) == list:
        return bencode_list(val)
    elif type(val) == dict:
        return bencode_dict(val)
    elif hasattr(val, "hex"):
        return bencode_bits(val)
    else:
        raise EncodeError(val)


def bencode_bits(bits):
    """
    bencode_bits

    Encode bytes.

    Args
    --------
    bits : bytes or bytearray
        string

    Returns
    ---------
    bytes:
         bencoded string
    """
    size = str(len(bits)) + ":"
    return size.encode("utf-8") + bits


def bencode_str(txt):
    """
    bencode_str

    Encode string types.

    Args
    --------
    txt (str): string


    Returns
    ---------
    bytes:
         bencoded string
    """
    size = str(len(txt)) + ":"
    return size.encode("utf-8") + txt.encode("utf-8")


def bencode_int(i):
    """
    bencode_int

    Encode integer type.

    Args
    --------
    i : int
        number that needs encoding

    Returns
    ---------
    bytes:
         bencoded int
    """
    return ("i" + str(i) + "e").encode("utf-8")


def bencode_list(elems):
    """
    bencode_list

    Encode list and contents.

    Args
    --------
    elems : list
        list of items for bencoding

    Returns
    ---------
    bytes:
         bencoded list and contents
    """
    arr = bytearray("l", encoding="utf-8")
    for elem in elems:
        encoded = benencode(elem)
        arr.extend(encoded)
    arr.extend(b"e")
    return arr


def bencode_dict(dic):
    """
    bencode_dict

    Encode dictionary and contents.

    Args
    --------
    dic : dict
        key,value pairs of items for bencoding.

    Returns
    ---------
    bytes:
         Bencoded key, value pairs of data.
    """
    result = b"d"
    for k, v in dic.items():
        result += b"".join([benencode(k), benencode(v)])
    return result + b"e"
