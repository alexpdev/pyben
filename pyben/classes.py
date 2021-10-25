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
OOP implementation of bencode decoders and encoders.

This style is not recommended as it can get bulky. The json-like api
from the bencode.py module is much easier to use.

Classes
-------
* Bendecoder
* Benencoder
"""

import os
import re

from pyben.exceptions import DecodeError, EncodeError


class Bendecoder:
    """Decode class contains all decode methods."""

    def __init__(self, data=None):
        """
        Initialize instance with optional pre compiled data.

        Args:
        ----
        data : `bytes` or `bytearray`
            (Optional) (default=None) Target data for decoding.

        """
        self.data = data
        self.decoded = None

    @classmethod
    def load(cls, item):
        """
        Extract contents from path/path-like and return Decoded data.

        Args
        ----
        path : `str` or `path-like`
            Path containing bencoded data.

        Raises
        ------
        `FilePathError`:
            Incorrect path or IOBuffer doesnt exist.

        Returns
        -------
        any
            Decoded contents of file, Usually a dictionary.

        """
        decoder = cls()
        if hasattr(item, "read"):
            data = item.read()

        elif os.path.exists(item) and os.path.isfile(item):
            with open(item, "rb") as _fd:
                data = _fd.read()
        return decoder.decode(data)

    @classmethod
    def loads(cls, data):
        """
        Shortcut to Decode raw bencoded data.

        Args
        ----
        data : ``bytes`` or `bytearray`
            Bendencoded `bytes`.

        Returns
        -------
        any
            Decoded data usually a dictionary.

        """
        decoder = cls()
        return decoder.decode(data)

    def decode(self, data=None):
        """
        Decode bencoded data.

        Args
        ----
        bits : ``bytes``
            bencoded data for decoding.

        Returns
        -------
        any :
            the decoded data.

        """
        data = self.data if not data else data
        self.decoded, _ = self._decode(bits=data)
        return self.decoded

    def _decode(self, bits=None):
        """
        Decode bencoded data.

        Args
        ----
        bits : ``bytes``
            Bencoded data for decoding.

        Returns
        -------
        any :
            The decoded data.

        """
        if bits.startswith(b"i"):
            match, feed = self._decode_int(bits)
            return match, feed

        # decode string
        if chr(bits[0]).isdigit():
            num, feed = self._decode_str(bits)
            return num, feed

        # decode list and contents
        if bits.startswith(b"l"):
            lst, feed = self._decode_list(bits)
            return lst, feed

        # decode dictionary and contents
        if bits.startswith(b"d"):
            dic, feed = self._decode_dict(bits)
            return dic, feed

        raise DecodeError(bits)

    def _decode_dict(self, bits):
        """
        Decode keys and values in dictionary.

        Args
        ----
        bits : ``bytes`` or `bytearray`
            `Bytes` of data for decoding.

        Returns
        -------
        `dict` :
            Dictionary and contents.

        """
        dct, feed = {}, 1
        while not bits[feed:].startswith(b"e"):
            match1, rest = self._decode(bits[feed:])
            feed += rest
            match2, rest = self._decode(bits[feed:])
            feed += rest
            dct[match1] = match2
        feed += 1
        return dct, feed

    def _decode_list(self, data):
        """
        Decode list and its contents.

        Args
        ----
        bits : `bytearray`
            Bencoded data.

        Returns
        -------
        `list`:
            decoded list and contents

        """
        seq, feed = [], 1
        while not data[feed:].startswith(b"e"):
            match, rest = self._decode(data[feed:])
            seq.append(match)
            feed += rest
        feed += 1
        return seq, feed

    @staticmethod
    def _decode_str(bits):
        """
        Decode string.

        Args
        ----
        bits : ``bytes`` or `bytearray`
            Bencoded string.

        Returns
        -------
        `str`:
            Decoded string.

        """
        match = re.match(br"(\d+):", bits)
        word_size, start = int(match.groups()[0]), match.span()[1]
        finish = start + word_size
        word = bits[start:finish]

        try:
            word = word.decode("utf-8")

        except UnicodeDecodeError:
            pass

        return word, finish

    @staticmethod
    def _decode_int(bits):
        """
        Decode integer type.

        Args
        ----
        bits : ``bytes`` or `bytearray`
            Bencoded intiger.

        Returns
        -------
        `int`:
            Decoded intiger.

        """
        obj = re.match(br"i(-?\d+)e", bits)
        return int(obj.group(1)), obj.end()


class Benencoder:
    """Encoder for bencode encoding used for Bittorrent meta-files."""

    def __init__(self, data=None):
        """
        Initialize Benencoder insance with optional pre compiled data.

        Args:
        ----
        data : any
            (Optional) Target data for encoding. Defaults to None.

        """
        self.data = data
        self.encoded = None

    @classmethod
    def dump(cls, data, path):
        """
        Shortcut Classmethod for encoding data and writing to file.

        Args
        ----
        data : any
            Raw data to be encoded, usually dict.txt
        path : path-like or `BytesIO`
            Where encoded data should be written to.py

        Returns
        -------
        `bool` : Return True if success.txt

        """
        encoded = cls(data).encode()
        if hasattr(path, "write"):
            path.write(encoded)
        else:
            with open(path, "wb") as _fd:
                _fd.write(encoded)
        return True

    @classmethod
    def dumps(cls, data):
        """
        Shortcut method for encoding data and immediately returning it.

        Args
        ----
        data : any
            Raw data to be encoded usually a dictionary.

        Returns
        -------
        `bytes`: Encoded data.

        """
        return cls(data).encode()

    def encode(self, val=None):
        """
        Encode data provided as an arguement or provided at initialization.

        Args
        ----
        val : any, optional
            Data for encoding. Defaults to None.

        Returns
        -------
        `bytes` : encoded data

        """
        if val is None:
            val = self.data
        self.encoded = self._encode(val)
        return self.encoded

    def _encode(self, val):
        """
        Encode data with bencode protocol.

        Args
        ----
        bits : `bytes`
            Bencoded data for decoding.

        Returns
        -------
        any : the decoded data.

        """
        if isinstance(val, str):
            return self._encode_str(val)

        if hasattr(val, "hex"):
            return self._encode_bytes(val)

        if isinstance(val, int):
            return self._encode_int(val)

        if isinstance(val, list):
            return self._encode_list(val)

        if isinstance(val, dict):
            return self._encode_dict(val)

        if isinstance(val, tuple):
            return self._encode_list(list(val))

        raise EncodeError(val)

    @staticmethod
    def _encode_bytes(val):
        """Bencode encoding bytes as string literal."""
        size = str(len(val)) + ":"
        return size.encode("utf-8") + val

    @staticmethod
    def _encode_str(txt):
        """
        Decode string.

        Args
        ----
        txt : `str`
            Any string literal.

        Returns
        -------
        `bytes` : Bencoded string.

        """
        size = str(len(txt)).encode("utf-8")
        return size + b":" + txt.encode("utf-8")

    @staticmethod
    def _encode_int(num):
        """
        Encode intiger.

        Args
        ----
        num : `int`
            Integer for encoding.

        Returns
        -------
        `bytes` : Bencoded intiger.

        """
        return b"i" + str(num).encode("utf-8") + b"e"

    def _encode_list(self, elems):
        """
        Encode list and its contents.

        Args
        ----
        elems : `list`
            List of content to be encoded.

        Returns
        -------
        `bytes` : Bencoded data

        """
        lst = [b"l"]
        for elem in elems:
            encoded = self._encode(elem)
            lst.append(encoded)
        lst.append(b"e")
        bit_lst = b"".join(lst)
        return bit_lst

    def _encode_dict(self, dic):
        """
        Encode keys and values in dictionary.

        Args
        ----
        dic : `dict`
            Dictionary of data for encoding.

        Returns
        -------
        `bytes` : Bencoded data.

        """
        result = b"d"
        for key, val in dic.items():
            result += b"".join([self._encode(key), self._encode(val)])
        return result + b"e"
