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
"""Testing module for Pyben package."""

import os
import shutil
from hashlib import sha256

import pyben


def rmpath(path):
    """Remove path."""
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def testmeta():
    """Create dummy metadata."""
    pieces_key = sha256("bcdfghjklmnpqrstvwxyz".encode("utf-8")).digest()
    pieces_val = sha256("aeiou".encode("utf-8")).digest()
    meta = {
        "announce": "http://ubuntu.com/announce",
        "info": {
            "name": "ubuntu.iso",
            "length": 12845738,
            "piece length": 262144,
            "private": 1,
            "source": "ubuntu",
        },
        "pieces root": {pieces_key: pieces_val},
        "created by": "mktorrent",
    }
    assert isinstance(meta, dict)  # nosec
    return meta


def testfile():
    """Create testing file."""
    parent = os.path.dirname(os.path.abspath(__file__))
    tfile = os.path.join(parent, "tempfile.pyben")
    meta = testmeta()
    with open(tfile, "wb") as fd:
        pyben.dump(meta, fd)
    assert os.path.exists(tfile)  # nosec
    return tfile


def ints():
    """Return integer tests."""
    return [
        (18, b"i18e"),
        (25, b"i25e"),
        (32, b"i32e"),
        (39, b"i39e"),
        (46, b"i46e"),
        (53, b"i53e"),
        (60, b"i60e"),
        (67, b"i67e"),
        (74, b"i74e"),
        (81, b"i81e"),
        (88, b"i88e"),
        (95, b"i95e"),
        (102, b"i102e"),
        (109, b"i109e"),
        (116, b"i116e"),
        (123, b"i123e"),
        (130, b"i130e"),
        (137, b"i137e"),
        (144, b"i144e"),
        (151, b"i151e"),
        (158, b"i158e"),
        (165, b"i165e"),
        (172, b"i172e"),
        (179, b"i179e"),
        (186, b"i186e"),
        (193, b"i193e"),
        (200, b"i200e"),
        (207, b"i207e"),
        (214, b"i214e"),
        (221, b"i221e"),
        (228, b"i228e"),
        (235, b"i235e"),
        (242, b"i242e"),
        (249, b"i249e"),
        (256, b"i256e"),
        (263, b"i263e"),
        (270, b"i270e"),
        (277, b"i277e"),
        (284, b"i284e"),
        (291, b"i291e"),
    ]


def strings():
    """Return string tests."""
    return [
        ("", b"0:"),
        ("Hello World", b"11:Hello World"),
        ("Television", b"10:Television"),
        ("Foo", b"3:Foo"),
        ("Bar", b"3:Bar"),
        ("Foo/Bar", b"7:Foo/Bar"),
        ("foobar", b"6:foobar"),
        ("foo:bar", b"7:foo:bar"),
        ("[foobar]baz", b"11:[foobar]baz"),
        ("Peter Parker", b"12:Peter Parker"),
        ("bruce wayne", b"11:bruce wayne"),
        ("tom and jerry", b"13:tom and jerry"),
        ("ben n' jerrys", b"13:ben n' jerrys"),
        ("sys", b"3:sys"),
        (")(*&^%$#$", b"9:)(*&^%$#$"),
        ("FOOBAR", b"6:FOOBAR"),
    ]


def lists():
    """Return list tests."""
    return [
        ([], b"le"),
        ([130, "foobar", "foo:bar"], b"li130e6:foobar7:foo:bare"),
        (
            ["Television", "Hello World", "Foo", 249, "[foobar]baz"],
            b"l10:Television11:Hello World3:Fooi249e11:[foobar]baze",
        ),
        (
            [
                "foo:bar",
                "tom and jerry",
                "FOOBAR",
                109,
                291,
                193,
                "foo:bar",
                291,
                "Foo/Bar",
            ],
            (
                b"l7:foo:bar13:tom and jerry6:FOOBARi109ei291ei193e7:foo:"
                b"bari291e7:Foo/Bare"
            ),
        ),
        (
            [
                130,
                "foobar",
                32,
                165,
                151,
                ")(*&^%$#$",
                53,
                221,
                32,
                193,
                53,
                "tom and jerry",
            ],
            (
                b"li130e6:foobari32ei165ei151e9:)(*&^%$#$i53ei221ei32ei193e"
                b"i53e13:tom and jerrye"
            ),
        ),
        (
            [
                "Television",
                "Foo",
                284,
                "Foo/Bar",
                256,
                25,
                25,
                "Hello World",
                151,
                "ben n' jerrys",
                "Peter Parker",
                "Foo",
                116,
                "FOOBAR",
            ],
            (
                b"l10:Television3:Fooi284e7:Foo/Bari256ei25ei25e"
                b"11:Hello Worldi151e13:ben n' jerrys"
                b"12:Peter Parker3:Fooi116e6:FOOBARe"
            ),
        ),
    ]


def tuples():
    """Return list tests."""
    return [
        (tuple(), b"le"),
        ((130, "foobar", "foo:bar"), b"li130e6:foobar7:foo:bare"),
        (
            ("Television", "Hello World", "Foo", 249, "[foobar]baz"),
            b"l10:Television11:Hello World3:Fooi249e11:[foobar]baze",
        ),
        (
            (
                "foo:bar",
                "tom and jerry",
                "FOOBAR",
                109,
                291,
                193,
                "foo:bar",
                291,
                "Foo/Bar",
            ),
            (
                b"l7:foo:bar13:tom and jerry6:FOOBARi109ei291ei193e7:foo:"
                b"bari291e7:Foo/Bare"
            ),
        ),
        (
            (
                130,
                "foobar",
                32,
                165,
                151,
                ")(*&^%$#$",
                53,
                221,
                32,
                193,
                53,
                "tom and jerry",
            ),
            (
                b"li130e6:foobari32ei165ei151e9:)(*&^%$#$i53ei221ei32ei193e"
                b"i53e13:tom and jerrye"
            ),
        ),
        (
            (
                "Television",
                "Foo",
                284,
                "Foo/Bar",
                256,
                25,
                25,
                "Hello World",
                151,
                "ben n' jerrys",
                "Peter Parker",
                "Foo",
                116,
                "FOOBAR",
            ),
            (
                b"l10:Television3:Fooi284e7:Foo/Bari256ei25ei25e"
                b"11:Hello Worldi151e13:ben n' jerrys"
                b"12:Peter Parker3:Fooi116e6:FOOBARe"
            ),
        ),
    ]


def dicts():
    """Return dictionary tests."""
    return [
        ({"sys": 39}, b"d3:sysi39ee"),
        (
            {
                137: "Foo",
                "Foo": 242,
                "sys": "ben n' jerrys",
                "FOOBAR": [
                    130,
                    "foobar",
                    32,
                    165,
                    151,
                    ")(*&^%$#$",
                    53,
                    221,
                    32,
                    193,
                    53,
                    "tom and jerry",
                ],
            },
            (
                b"di137e3:Foo3:Fooi242e3:sys13:ben n' "
                b"jerrys6:FOOBARli130e6:foobari32ei165ei151e9:)(*&"
                b"^%$#$i53ei221ei32ei193ei53e13:tom and jerryee"
            ),
        ),
        (
            {
                "[foobar]baz": "tom and jerry",
                200: "Foo",
                "FOOBAR": 53,
                130: "ben n' jerrys",
                193: "Bar",
                109: "bruce wayne",
            },
            (
                b"d11:[foobar]baz13:tom and jerryi200e3:Foo6:FOOBARi53e"
                b"i130e13:ben n' jerrysi193e3:Bari109e11:bruce waynee"
            ),
        ),
        (
            {
                200: 165,
                32: 88,
                242: "sys",
                ")(*&^%$#$": "foobar",
                "ben n' jerrys": ")(*&^%$#$",
                "Foo": 116,
                "Foo/Bar": ")(*&^%$#$",
                "bruce wayne": 270,
            },
            (
                b"di200ei165ei32ei88ei242e3:sys9:)(*&^%$#$6:foobar13:ben n'"
                b" jerrys9:)(*&^%$#$3:Fooi116e7:Foo/Bar9:)(*&^%$#$11:bruce "
                b"waynei270ee"
            ),
        ),
        (
            {
                "Peter Parker": [130, "foobar", "foo:bar"],
                130: "Foo/Bar",
                "Foo": "sys",
                18: 263,
                "FOOBAR": [
                    "foo:bar",
                    "tom and jerry",
                    "FOOBAR",
                    109,
                    291,
                    193,
                    "foo:bar",
                    291,
                    "Foo/Bar",
                ],
                221: ")(*&^%$#$",
                39: 270,
                74: "tom and jerry",
                ")(*&^%$#$": "Bar",
                "bruce wayne": 193,
                "ben n' jerrys": "ben n' jerrys",
                "Foo/Bar": 95,
            },
            (
                b"d12:Peter Parkerli130e6:foobar7:foo:barei130e7:Foo/"
                b"Bar3:Foo3:sysi18ei263e6:FOOBARl7:foo:bar13:tom and "
                b"jerry6:FOOBARi109ei291ei193e7:foo:bari291e7:Foo/"
                b"Barei221e9:)(*&^%$#$i39ei270ei74e13:tom and jerry9:)"
                b"(*&^%$#$3:Bar11:bruce waynei193e13:ben n' jerrys"
                b"13:ben n' jerrys7:Foo/Bari95ee"
            ),
        ),
    ]


def data():
    """Return all test data types as one list."""
    lst = ints() + strings() + dicts() + lists()
    return lst
