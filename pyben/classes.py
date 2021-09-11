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

import os
import re
import json
from pyben.exceptions import FilePathError, DecodeError, EncodeError

class Bendecoder:
    """Decode class contains all decode methods."""

    def __init__(self, data=None):
        """
        Initialize instance with optional pre compiled data.

        Args
        --------
            data (bytes-like, optional): target data for decoding.
        """
        self.data = data
        self.decoded = None
        self.json = None

    @classmethod
    def load(cls, item):
        """
        Bendecoder.load(item)

        Extract contents from path/path-like and return Decoded data.

        Args
        --------
        path : str or IOBuffer
            Path containing bencoded data.

        Raises
        ---------
        FilePathError
            Incorrect path or IOBuffer doesnt exist.

        Returns
        ---------
        any
            Decoded contents of file, Usually a dictionary.
        """
        decoder = cls()
        if hasattr(item, "read"):
            data = item.read()
            return decoder.decode(data)
        elif os.path.exists(item) and os.path.isfile(item):
            with open(item, "rb") as fd:
                data = fd.read()
                return decoder.decode(data)
        raise FilePathError()

    @classmethod
    def loads(cls, data):
        """
        Benencoder.loads(data)

        Shortcut to Decode raw bencoded data.

        Args
        --------
        data : bytes
            Bendencoded bytes.

        Returns
        ---------
        any
            Decoded data usually a dictionary.
        """
        decoder = cls()
        return decoder.decode(data)

    def decode(self, data=None):
        """
        Decode bencoded data.

        Args
        -------
        bits : bytes
            bencoded data for decoding.

        Returns
        --------
        any
            the decoded data.
        """
        data = self.data if not data else data
        self.decoded, _ = self._decode(bits=data)
        return self.decoded

    def json(self, bits=None):
        """Return output of the decoder json serialized."""
        if not bits:
            if self.decoded is None:
                self.decoded = self.decode(self.data)
        else:
            self.decoded = self.decode(bits)
        self.json = json.dumps(self.decoded)
        return self.json

    def _decode(self, bits=None):
        if bits is None:
            bits = self.data
        if bits.startswith(b"i"):
            match, feed = self._decode_int(bits)
            return match, feed

        # decode string
        elif chr(bits[0]).isdigit():
            num, feed = self._decode_str(bits)
            return num, feed

        # decode list and contents
        elif bits.startswith(b"l"):
            lst, feed = self._decode_list(bits)
            return lst, feed

        # decode dictionary and contents
        elif bits.startswith(b"d"):
            dic, feed = self._decode_dict(bits)
            return dic, feed
        else:
            raise DecodeError(bits, "Unrecognized data. Cannot decode.")

    def _decode_dict(self, bits):
        """
        Decode keys and values in dictionary.

        Args
        --------
        bits (bytearray): bytes of data for decoding.

        Returns
        ---------
        [dict]
            : dictionary and contents.
        """
        dic, feed = {}, 1
        while not bits[feed:].startswith(b"e"):
            match1, rest = self._decode(bits[feed:])
            feed += rest
            match2, rest = self._decode(bits[feed:])
            feed += rest
            dic[match1] = match2
        feed += 1
        return dic, feed

    def _decode_list(self, bits):
        """
        Decode list and its contents.

        Args
        --------
        bits : bytearray
            Bencoded data.

        Returns
        ---------
        list
            : decoded list and contents
        """
        lst, feed = [], 1
        while not bits[feed:].startswith(b"e"):
            match, rest = self._decode(bits[feed:])
            lst.append(match)
            feed += rest
        feed += 1
        return lst, feed

    def _decode_str(self, bits):
        """
        Decode string.

        Args
        --------
        bits (bytearray): bencoded string.

        Returns
        ---------
        [str]
            : decoded string.
        """
        match = re.match(br"(\d+):", bits)
        word_len, start = int(match.groups()[0]), match.span()[1]
        word = bits[start : start + word_len]
        try:
            word = word.decode("utf-8")
        except:
            word = word.hex()
        return word, start + word_len

    def _decode_int(self, bits):
        """
        Decode intiger.

        Args
        --------
        bits (bytearray): bencoded intiger.

        Returns
        ---------
        [int]
            : decoded intiger.
        """
        obj = re.match(br"i(-?\d+)e", bits)
        return int(obj.group(1)), obj.end()


class Benencoder:
    """Encode collection of methods for Bencoding data."""

    def __init__(self, data=None):
        """
        Initialize Benencoder insance with optional pre compiled data.

        Args
        --------
        data : any, optional
            Target data for encoding. Defaults to None.
        """
        self.data = data
        self.encoded = None

    @classmethod
    def dump(cls, data, path):
        """
        Benecoder.dump(data,path)

        Shortcut Classmethod for encoding data and writing to file. This

        Args
        --------
        data : any
            Raw data to be encoded, usually dict.txt
        path : path-like or iobuffer
            Where encoded data should be written to.py

        Returns
        ---------
        bool:
             Return True if success.txt
        """
        encoded = cls(data).encode()
        if hasattr(path, "write"):
            path.write(encoded)
        else:
            with open(path, "wb") as fd:
                fd.write(encoded)
        return True

    @classmethod
    def dumps(cls, data):
        """
        self.dumps(data)

        Shortcut method for encoding data and immediately returning it.

        Args
        --------
        data : any
            Raw data to be encoded usually a dictionary.

        Returns
        ---------
        bytes:
             encoded data.
        """
        return cls(data).encode()

    def encode(self, val=None):
        """
        self.encode(val)

        Encodes data provided as an arguement or provided at initialization.

        Args
        --------
        val : any, optional
            Data for encoding. Defaults to None.

        Returns
        ---------
        bytes:
             encoded data
        """
        if val is None:
            val = self.data
        self.encoded = self._encode(val)
        return self.encoded

    def _encode(self, val):
        """
        self._encode(val)

        Encode data with bencode protocol.

        args
        --------
        bits : bytes
            Bencoded data for decoding.

        returns
        ---------
        any:
             the decoded data.
        """
        if type(val) == str:
            return self._encode_str(val)

        if hasattr(val, "hex"):
            return self._encode_bytes(val)

        elif type(val) == int:
            return self._encode_int(val)

        elif type(val) == list:
            return self._encode_list(val)

        elif type(val) == dict:
            return self._encode_dict(val)

        raise EncodeError(val)

    def _encode_bytes(self, val):
        size = str(len(val)) + ":"
        return size.encode("utf-8") + val

    def _encode_str(self, txt):
        """
        _encode_str(self, txt)

        Decode string.

        Args
        --------
        txt (str): string.

        Returns
        ---------
        [bytes]
            : bencoded string.
        """
        size = str(len(txt)).encode("utf-8")
        return size + b":" + txt.encode("utf-8")

    def _encode_int(self, i):
        """
        _encode_int(self,i)

        Encode intiger.

        Args
        --------
        i : int
            Intiger

        Returns
        ---------
        bytes
            : bencoded intiger.
        """
        return b"i" + str(i).encode("utf-8") + b"e"

    def _encode_list(self, elems):
        """Encode list and its contents.

        Args
        --------
        elems : list
            List of content to be encoded.

        Returns
        ---------
        bytes
            : bencoded data
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
        --------
        dic : dict
            Dictionary of data for encoding.

        Returns
        ---------
        bytes
            Bencoded data.
        """
        result = b"d"
        for k, v in dic.items():
            result += b"".join([self._encode(k), self._encode(v)])
        return result + b"e"
