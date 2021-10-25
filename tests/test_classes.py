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
from pyben.exceptions import DecodeError, EncodeError

from .context import (data, dicts, ints, lists, rmpath, strings, testfile,
                      testmeta)


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


@pytest.mark.parametrize("decoded, encoded", strings())
def test_decoder_constructor(decoded, encoded):
    """Test Bendecoder constructor."""
    decoder = Bendecoder(encoded)
    decode = decoder.decode()
    assert decode == decoded  # nosec


def test_malformed_data():
    """Test data that cannot be interpreted by decoder."""
    data = b"li92e12:hello world!::e"
    decoder = Bendecoder(data)
    try:
        _ = decoder.decode()
    except DecodeError:
        assert True  # nosec


def test_improper_type():
    """Test type that isn't interpreted by encoder."""
    vals = {1, 2, 3, 4, 5}
    data = [12, "hello world!", vals]
    encoder = Benencoder(data)
    try:
        _ = encoder.encode()
    except EncodeError:
        assert True  # nosec


def test_encode_tuple_to_list():
    """Test encoding tuple to list."""
    data = ((130, "foobar", "foo:bar"), b"li130e6:foobar7:foo:bare")
    assert Benencoder()._encode_list(data[0]) == data[1]  # nosec


def test_encode_tuple_cast():
    """Test encoding tuple to list main method."""
    data = ((130, "foobar", "foo:bar"), b"li130e6:foobar7:foo:bare")
    assert Benencoder().encode(data[0]) == data[1]  # nosec


@pytest.mark.parametrize("decoded, encoded", strings())
def test_decode_str(decoded, encoded):
    """Test string decoding."""
    decoder = Bendecoder()
    text, _ = decoder._decode_str(encoded)
    assert decoded == text  # nosec


@pytest.mark.parametrize("decoded, encoded", ints())
def test_decode_int_class(decoded, encoded):
    """Test integer decoding."""
    decoder = Bendecoder()
    real, _ = decoder._decode_int(encoded)
    assert real == decoded  # nosec


@pytest.mark.parametrize("decoded, encoded", lists())
def test_decode_list_class(decoded, encoded):
    """Test list decoding."""
    decoder = Bendecoder()
    decode, _ = decoder._decode_list(encoded)
    assert decode == decoded  # nosec


@pytest.mark.parametrize("decoded, encoded", dicts())
def test_decode_dict_class(decoded, encoded):
    """Test dictionary decoding."""
    decoder = Bendecoder()
    decode, _ = decoder._decode_dict(encoded)
    assert decoded == decode  # nosec


@pytest.mark.parametrize("decoded, encoded", data())
def test_decode_class(decoded, encoded):
    """Test decoding."""
    decoder = Bendecoder()
    item = decoder.decode(encoded)
    assert decoded == item  # nosec


def test_decode_load(tfile):
    """Test inline decoding."""
    decoder = Bendecoder()
    output = decoder.load(tfile)
    assert isinstance(output, dict)  # nosec


def test_decode_loads(tfile):
    """Test from file decoding."""
    with open(tfile, "rb") as _fd:
        inp = _fd.read()
    decoder = Bendecoder()
    out = decoder.loads(inp)
    assert out["info"]["length"] == 12845738  # nosec


@pytest.mark.parametrize("decoded, encoded", strings())
def test_bencode_str(decoded, encoded):
    """Test string encoding."""
    encoder = Benencoder()
    text = encoder._encode_str(decoded)
    assert encoded == text  # nosec


@pytest.mark.parametrize("decoded, encoded", ints())
def test_bencode_int(decoded, encoded):
    """Test integer encoding."""
    encoder = Benencoder()
    real = encoder._encode_int(decoded)
    assert real == encoded  # nosec


@pytest.mark.parametrize("decoded, encoded", lists())
def test_bencode_list(decoded, encoded):
    """Test list encoding."""
    encoder = Benencoder()
    benlist = encoder._encode_list(decoded)
    assert encoded == benlist  # nosec


def test_bencode_dump(tmeta, tfile):
    """Test to file encoding with path string."""
    encoder = Benencoder()
    encoder.dump(tmeta, tfile)
    assert os.path.exists(tfile)  # nosec


def test_bencode_dump1(tmeta, tfile):
    """Test to file encoding with FileIO."""
    encoder = Benencoder()
    with open(tfile, "wb") as a:
        encoder.dump(tmeta, a)
    assert os.path.exists(tfile)  # nosec


def test_bencode_dumps(tmeta):
    """Test inline encoding."""
    encoder = Benencoder()
    reg = encoder.dumps(tmeta)
    assert isinstance(reg, bytes)  # nosec


@pytest.mark.parametrize("decoded, encoded", dicts())
def test_encode_dict(decoded, encoded):
    """Test dictionary encoding."""
    encoder = Benencoder()
    bendict = encoder._encode_dict(decoded)
    assert bendict == encoded  # nosec


@pytest.mark.parametrize("decoded, encoded", data())
def test_encode(decoded, encoded):
    """Test encoding."""
    encoder = Benencoder()
    benitem = encoder.encode(decoded)
    assert encoded == benitem  # nosec


def test_bendecoder_load(tfile):
    """Test inline decoding."""
    decoder = Bendecoder()
    with open(tfile, "rb") as _fd:
        data = decoder.load(_fd)
    assert data is not None  # nosec


@pytest.mark.parametrize("decoded, encoded", lists())
def test_decoder_bits(decoded, encoded):
    """Test inline decoding with classes."""
    decoder = Bendecoder(encoded)
    lst = decoder.decode()
    assert decoded == lst  # nosec
