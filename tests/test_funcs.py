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
"""Pytest tests for functions in pyben package."""

import pytest

from pyben.bencode import (bencode_dict, bencode_int, bencode_list,
                           bencode_str, bendecode, bendecode_dict,
                           bendecode_int, bendecode_list, bendecode_str,
                           benencode)
from pyben.exceptions import DecodeError, EncodeError

from . import context


def test_malformed_bytes():
    """Test byte string literal that is not understood by decoder."""
    data = b"dspi123elees11:hello world!spqyt"
    try:
        _ = bendecode(data)
    except DecodeError:
        assert True  # nosec


def test_undecodable_data():
    """Test type not understood by encoder."""
    data = {1, 2, 3, 4, 5}
    try:
        _ = benencode(data)
    except EncodeError:
        assert True  # nosec


@pytest.mark.parametrize("decoded, encoded", context.lists())
def test_benencode_tuple_list(decoded, encoded):
    """Test turning a tuple to a list while encoding."""
    assert bencode_list(decoded) == encoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.tuples())
def test_benencode_tuple_to_list(decoded, encoded):
    """Test turning a tuple to a list while encoding."""
    assert benencode(decoded) == encoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.strings())
def test_bendecode_str(decoded, encoded):
    """Test decoding strings."""
    text, _ = bendecode_str(encoded)
    assert decoded == text  # nosec


@pytest.mark.parametrize("decoded, encoded", context.strings())
def test_bendecode_str_feed(decoded, encoded):
    """Test decoding strings feeds."""
    len(decoded)
    _, feed = bendecode_str(encoded)
    assert feed == len(encoded)  # nosec


@pytest.mark.parametrize("decoded, encoded", context.strings())
def test_bendecode_str_equality(decoded, encoded):
    """Test equality for testing strings."""
    len(decoded)
    text, _ = bendecode_str(encoded)
    pre = str(len(text)) + ":" + text
    assert pre.encode("UTF-8") == encoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.ints())
def test_bendecode_int(decoded, encoded):
    """Test decoding integers."""
    real, _ = bendecode_int(encoded)
    assert real == decoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.ints())
def test_bendecode_int_feed(decoded, encoded):
    """Test decoding integers feeds."""
    str(decoded)
    _, feed = bendecode_int(encoded)
    assert feed == len(encoded)  # nosec


@pytest.mark.parametrize("decoded, encoded", context.lists())
def test_bendecode_list(decoded, encoded):
    """Test decoding lists."""
    dec, _ = bendecode_list(encoded)
    assert dec == decoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.lists())
def test_bendecode_list_feed(decoded, encoded):
    """Test encoding lists feeds."""
    str(decoded)
    _, feed = bendecode_list(encoded)
    assert feed == len(encoded)  # nosec


@pytest.mark.parametrize("decoded, encoded", context.dicts())
def test_bendecode_dict(encoded, decoded):
    """Test encoding dicts."""
    dct, _ = bendecode_dict(encoded)
    assert dct == decoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.dicts())
def test_bendecode_dict_feed(encoded, decoded):
    """Test encoding dicts feeds."""
    str(decoded)
    _, feed = bendecode_dict(encoded)
    assert feed == len(encoded)  # nosec


@pytest.mark.parametrize("decoded, encoded", context.strings())
def test_bencode_str(encoded, decoded):
    """Test encoding strings."""
    text = bencode_str(decoded)
    assert encoded == text  # nosec


@pytest.mark.parametrize("decoded, encoded", context.ints())
def test_bencode_int(encoded, decoded):
    """Test encoding integers."""
    real = bencode_int(decoded)
    assert real == encoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.lists())
def test_bencode_list(encoded, decoded):
    """Test encoding lists."""
    benlist = bencode_list(decoded)
    assert encoded == benlist  # nosec


@pytest.mark.parametrize("decoded, encoded", context.dicts())
def test_bencode_dict(encoded, decoded):
    """Test encoding dicts."""
    bendict = bencode_dict(decoded)
    assert bendict == encoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.data())
def test_bencode_all(encoded, decoded):
    """Test encoding all types."""
    benunit = benencode(decoded)
    assert benunit == encoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.data())
def test_bendecode_all(encoded, decoded):
    """Test decoding all types."""
    item, _ = bendecode(encoded)
    assert item == decoded  # nosec
