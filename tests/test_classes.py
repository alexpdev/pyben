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
"""Testing PyBen OOP implementation.

Example of single file .torrent metadata:

    tfile={
        "announce": "http://ubuntu.com/announce",
        "info": {
            "name": "ubuntu.iso",
            "length": 12845678
            "piece length": 262144,
            "private": 1,
            "source": "ubuntu",
        },
    "created by": "mktorrent",
    "creation date": 20398488923,
    }

"""

import os
import pytest
from pyben.classes import Bendecoder, Benencoder
from . import ints, strings, dicts, lists, testmeta, testfile, rmpath


@pytest.fixture
def tfile():
    """Testfile Pytest fixture."""
    tempfile = testfile()
    yield tempfile
    rmpath(tempfile)


@pytest.fixture
def tmeta():
    """Metadata Pytest fixture."""
    info = testmeta()
    return info


@pytest.fixture
def types():
    """Return fixtures."""
    return [lists, ints, strings, dicts]


def test_types(types):
    """Test fixture functionality."""
    assert len(types) > 1


def test_encode_tuple_to_list_encode_list_method():
    """Test encoding tuple to list."""
    data = ((130, "foobar", "foo:bar"), b"li130e6:foobar7:foo:bare")
    assert Benencoder()._encode_list(data[0]) == data[1]


def test_encode_tuple_to_list_encode_method():
    """Test encoding tuple to list main method."""
    data = ((130, "foobar", "foo:bar"), b"li130e6:foobar7:foo:bare")
    assert Benencoder().encode(data[0]) == data[1]


def test_decode_str(strings):
    """Test string decoding."""
    decoder = Bendecoder()
    for string, benstring in strings:
        text, feed = decoder._decode_str(benstring)
        assert string == text
        assert feed == len(benstring)


def test_decode_int_class(ints):
    """Test integer decoding."""
    decoder = Bendecoder()
    for num, benint in ints:
        real, feed = decoder._decode_int(benint)
        assert real == num
        assert feed == len(benint)


def test_decode_list_class(lists):
    """Test list decoding."""
    decoder = Bendecoder()
    for lst, benlist in lists:
        decoded, _ = decoder._decode_list(benlist)
        assert decoded == lst


def test_decode_dict_class(dicts):
    """Test dictionary decoding."""
    decoder = Bendecoder()
    for dct, bendict in dicts:
        decoded, _ = decoder._decode_dict(bendict)
        assert dct == decoded


def test_decode_class(ints, strings, lists, dicts):
    """Test decoding."""
    data = [lists, strings, ints, dicts]
    decoder = Bendecoder()
    for val in data:
        for item, benitem in val:
            decoded = decoder.decode(benitem)
            assert decoded == item


def test_decode_load(tfile):
    """Test inline decoding."""
    decoder = Bendecoder()
    output = decoder.load(tfile)
    assert isinstance(output, dict)


def test_decode_loads(tfile):
    """Test from file decoding."""
    with open(tfile, "rb") as _fd:
        inp = _fd.read()
    decoder = Bendecoder()
    out = decoder.loads(inp)
    assert out["info"]["length"] == 12845738


def test_bencode_str(strings):
    """Test string encoding."""
    encoder = Benencoder()
    for string, benstring in strings:
        text = encoder._encode_str(string)
        assert benstring == text


def test_bencode_int(ints):
    """Test integer encoding."""
    encoder = Benencoder()
    for num, benint in ints:
        real = encoder._encode_int(num)
        assert real == benint


def test_bencode_list(lists):
    """Test list encoding."""
    encoder = Benencoder()
    for lst, benlist in lists:
        encoded = encoder._encode_list(lst)
        assert encoded == benlist


def test_bencode_dump(tmeta, tfile):
    """Test to file encoding with path string."""
    encoder = Benencoder()
    encoder.dump(tmeta, tfile)
    assert os.path.exists(tfile)


def test_bencode_dump1(tmeta, tfile):
    """Test to file encoding with FileIO."""
    encoder = Benencoder()
    with open(tfile, "wb") as a:
        encoder.dump(tmeta, a)
    assert os.path.exists(tfile)


def test_bencode_dumps(tmeta):
    """Test inline encoding."""
    encoder = Benencoder()
    reg = encoder.dumps(tmeta)
    assert isinstance(reg, bytes)


def test_encode_dict(dicts):
    """Test dictionary encoding."""
    encoder = Benencoder()
    for dct, bendict in dicts:
        encoded = encoder._encode_dict(dct)
        assert bendict == encoded


def test_encode(ints, strings, lists, dicts):
    """Test encoding."""
    data = [ints, strings, lists, dicts]
    encoder = Benencoder()
    for val in data:
        for item, benitem in val:
            encoded = encoder.encode(item)
            assert encoded == benitem


def test_bendecoder_load(tfile):
    """Test inline decoding."""
    decoder = Bendecoder()
    with open(tfile, "rb") as _fd:
        data = decoder.load(_fd)
    assert data is not None
