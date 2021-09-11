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

import pytest
from tests.testdata import data
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


@pytest.fixture
def numbers():
    ints = data[0]
    return ints


@pytest.fixture
def strings():
    text = data[-1]
    return text


@pytest.fixture
def dicts():
    dictionaries = data[1]
    return dictionaries


@pytest.fixture
def lists():
    arrays = data[2]
    return arrays


@pytest.fixture
def tdata():
    return data


def test_bendecode_str(strings):
    for string, benstring in strings:
        text, feed = bendecode_str(benstring)
        assert string == text
        assert feed == len(benstring)


def test_bendecode_str_equality(strings):
    for _, benstring in strings:
        text, _ = bendecode_str(benstring)
        assert (str(len(text)) + ":" + text).encode("UTF-8") == benstring


def test_bendecode_int(numbers):
    for num, benint in numbers:
        real, feed = bendecode_int(benint)
        assert real == num
        assert feed == len(benint)


def test_bendecode_list(lists):
    for lst, benlist in lists:
        decoded, feed = bendecode_list(benlist)
        assert decoded == lst
        assert feed == len(benlist)


def test_bendecode_dict(dicts):
    for dct, bendict in dicts:
        decoded, feed = bendecode_dict(bendict)
        assert dct == decoded
        assert feed == len(bendict)


def test_decode(tdata):
    for data in tdata:
        for item, benitem in data:
            decoded, feed = bendecode(benitem)
            assert decoded == item
            assert feed == len(benitem)


def test_bencode_str(strings):
    for string, benstring in strings:
        text = bencode_str(string)
        assert benstring == text


def test_bencode_int(numbers):
    for num, benint in numbers:
        real = bencode_int(num)
        assert real == benint


def test_bencode_list(lists):
    for lst, benlist in lists:
        encoded = bencode_list(lst)
        assert encoded == benlist


def test_bencode_dict(dicts):
    for dct, bendict in dicts:
        encoded = bencode_dict(dct)
        assert bendict == encoded


def test_bencode(tdata):
    for data in tdata:
        for item, benitem in data:
            encoded = benencode(item)
            assert encoded == benitem
