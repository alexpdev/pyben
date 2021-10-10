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
from pyben.bencode import (
    bendecode,
    benencode,
    bendecode_str,
    bendecode_int,
    bendecode_list,
    bendecode_dict,
    bencode_str,
    bencode_int,
    bencode_list,
    bencode_dict,
)
from . import ints, strings, dicts, lists


@pytest.fixture
def metadata():
    """Pytest fixture functionality test fixture."""
    return ints, strings, dicts, lists


def test_matadata(metadata):
    """Pytest fixture functionality test."""
    assert len(metadata) > 1


def test_benencode_tuple_list():
    """Test turning a tuple to a list while encoding."""
    lst = (130, "foobar", "foo:bar")
    assert bencode_list(lst) == b"li130e6:foobar7:foo:bare"


def test_benencode_tuple_to_list():
    """Test turning a tuple to a list while encoding."""
    lst = (130, "foobar", "foo:bar")
    assert benencode(lst) == b"li130e6:foobar7:foo:bare"


def test_bendecode_str(strings):
    """Test decoding strings."""
    for string, benstring in strings:
        text, _ = bendecode_str(benstring)
        assert string == text


def test_bendecode_str_feed(strings):
    """Test decoding strings feeds."""
    for _, benstring in strings:
        _, feed = bendecode_str(benstring)
        assert feed == len(benstring)


def test_bendecode_str_equality(strings):
    """Test equality for testing strings"""
    for _, benstring in strings:
        text, _ = bendecode_str(benstring)
        assert (str(len(text)) + ":" + text).encode("UTF-8") == benstring


def test_bendecode_int(ints):
    """Test decoding integers."""
    for num, benint in ints:
        real, _ = bendecode_int(benint)
        assert real == num


def test_bendecode_int_feed(ints):
    """Test decoding integers feeds."""
    for _, benint in ints:
        _, feed = bendecode_int(benint)
        assert feed == len(benint)


def test_bendecode_list(lists):
    """Test decoding lists."""
    for lst, benlist in lists:
        decoded, _ = bendecode_list(benlist)
        assert decoded == lst


def test_bendecode_list_feed(lists):
    """Test encoding lists feeds."""
    for _, benlist in lists:
        _, feed = bendecode_list(benlist)
        assert feed == len(benlist)


def test_bendecode_dict(dicts):
    """Test encoding dicts."""
    for dct, bendict in dicts:
        decoded, _ = bendecode_dict(bendict)
        assert dct == decoded


def test_bendecode_dict_feed(dicts):
    """Test encoding dicts feeds."""
    for _, bendict in dicts:
        _, feed = bendecode_dict(bendict)
        assert feed == len(bendict)


def test_bencode_str(strings):
    """Test encoding strings."""
    for string, benstring in strings:
        text = bencode_str(string)
        assert benstring == text


def test_bencode_int(ints):
    """Test encoding integers."""
    for num, benint in ints:
        real = bencode_int(num)
        assert real == benint


def test_bencode_list(lists):
    """Test encoding lists."""
    for lst, benlist in lists:
        encoded = bencode_list(lst)
        assert encoded == benlist


def test_bencode_dict(dicts):
    """Test encoding dicts."""
    for dct, bendict in dicts:
        encoded = bencode_dict(dct)
        assert bendict == encoded


def test_bencode_all(ints, strings, dicts, lists):
    """Test encoding all types."""
    data = [ints, strings, dicts, lists]
    for category in data:
        for unit, benunit in category:
            encoded = benencode(unit)
            assert benunit == encoded


def test_bendecode_all(ints, strings, dicts, lists):
    """Test decoding all types."""
    data = [ints, strings, dicts, lists]
    for category in data:
        for unit, benunit in category:
            decoded, _ = bendecode(benunit)
            assert unit == decoded
