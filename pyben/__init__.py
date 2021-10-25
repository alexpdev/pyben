#! /usr/bin/python3
# -*- coding: utf-8 -*-

#####################################################################
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#####################################################################
"""
PyBen is a library for decoding/encoding data, with the bencode specification.

Bencode is commonly used for encoding Bittorrent Protocol Metafiles (.torrent).

Modules
---------
* api
* classes
* bencode

Classes
---------
* Bendecoder
* Benencoder

Functions
---------
* bendecode
* benencode
* dump
* dumps
* load
* loads

"""

from pyben import api, bencode, classes
from pyben.api import dump, dumps, load, loads
from pyben.bencode import bendecode, benencode
from pyben.classes import Bendecoder, Benencoder

__version__ = "0.2.4"
__author__ = "alexpdev"

__all__ = [
    "Bendecoder",
    "Benencoder",
    "api",
    "bencode",
    "bendecode",
    "benencode",
    "classes",
    "dump",
    "dumps",
    "load",
    "loads",
]
