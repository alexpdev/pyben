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
from tests import TestBase


class TestDecodeFuncs(TestBase):
    def test_bendecode_str(self):
        for string, benstring in self.strings:
            text, feed = bendecode_str(benstring)
            assert string == text
            assert feed == len(benstring)

    def test_bendecode_int(self):
        for num, benint in self.ints:
            real, feed = bendecode_int(benint)
            assert real == num
            assert feed == len(benint)

    def test_bendecode_list(self):
        for lst, benlist in self.lists:
            decoded, feed = bendecode_list(benlist)
            assert decoded == lst
            assert feed == len(benlist)

    def test_bendecode_dict(self):
        for dct, bendict in self.dicts:
            decoded, feed = bendecode_dict(bendict)
            assert dct == decoded
            assert feed == len(bendict)

    def test_decode(self):
        for data in self.data:
            for item, benitem in data:
                decoded, feed = bendecode(benitem)
                assert decoded == item
                assert feed == len(benitem)


class TestEncodeFuncs(TestBase):
    def test_bencode_str(self):
        for string, benstring in self.strings:
            text = bencode_str(string)
            assert benstring == text

    def test_bencode_int(self):
        for num, benint in self.ints:
            real = bencode_int(num)
            assert real == benint

    def test_bendecode_list(self):
        for lst, benlist in self.lists:
            encoded = bencode_list(lst)
            assert encoded == benlist

    def test_bendecode_dict(self):
        for dct, bendict in self.dicts:
            encoded = bencode_dict(dct)
            assert bendict == encoded

    def test_decode(self):
        for data in self.data:
            for item, benitem in data:
                encoded = benencode(item)
                assert encoded == benitem
