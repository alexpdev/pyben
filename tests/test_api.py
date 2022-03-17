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
"""Testing functions for Pyben API module."""

import json
import os

import pytest

import pyben
from tests import context


@pytest.fixture
def tempfile():
    """Pytest Fixture providing temporary file."""
    fd = context.testfile()
    yield fd
    context.rmpath(fd)


@pytest.fixture
def tempmeta():
    """Pytest Fixture providing dummy meta data."""
    parent = os.path.dirname(os.path.abspath(__file__))
    tfile = os.path.join(parent, "tempfile.pyben")
    meta = context.testmeta()
    return meta, tfile


def test_writing_unicode(tempmeta):
    """Test Unicode support for writing bencode."""
    meta, tfile = tempmeta
    parent = os.path.dirname(tfile)
    txt = "测试测试测试测试.pyben"
    path = os.path.join(parent, txt)
    pyben.dump(meta, path)
    assert os.path.exists(path)
    context.rmpath(path)


def test_reading_unicode(tempmeta):
    """Test Unicode support for reading bencode."""
    path = os.path.join(os.path.dirname(tempmeta[1]), "测试测试测试测试.pyben")
    pyben.dump(tempmeta[0], path)
    meta = pyben.load(path)
    assert isinstance(meta, dict)
    context.rmpath(path)


def test_rmpath():
    """Test rmpath function."""
    path = "test_folder"
    os.mkdir(path)
    file_path1 = os.path.join(path, "rmpath_test_file1")
    file_path2 = os.path.join(path, "rmpath_test_file2")
    with open(file_path1, "wt") as test_file:
        test_file.write("Testing rmpath function in tests module.")
    with open(file_path2, "wt") as test_file:
        test_file.write("Testing rmpath function in tests module.")
    context.rmpath(path)
    assert not os.path.exists("rmpath_test_file")


def test_api_tuple_to_list():
    """Test encoding tuple to list."""
    lst = (130, "foobar", "foo:bar")
    assert pyben.dumps(lst) == b"li130e6:foobar7:foo:bare"


@pytest.mark.parametrize("decoded, encoded", context.data())
def test_api_loads(decoded, encoded):
    """Test decoding inline."""
    assert pyben.loads(encoded) == decoded


@pytest.mark.parametrize("decoded, encoded", context.data())
def test_api_dumps(decoded, encoded):
    """Test encoding inline."""
    assert pyben.dumps(decoded) == encoded


def test_api_loads_exists(tempfile):
    """Test decoding from file."""
    fd = tempfile
    assert os.path.exists(fd)


def test_api_loads_type(tempfile):
    """Test inline encoding type."""
    decoded = pyben.load(tempfile)
    assert isinstance(decoded, dict)


def test_api_loads_containes(tempfile):
    """Test inline decoding containers."""
    decoded = pyben.load(tempfile)
    assert "ubuntu.com" in decoded["announce"].lower()


def test_api_dump_string(tempmeta):
    """Test encoding to file."""
    meta, path = tempmeta
    pyben.dump(meta, path)
    assert os.path.exists(path)
    context.rmpath(path)


def test_api_with_file_load(tempfile):
    """Test load function with opened BytesIO."""
    with open(tempfile, "rb") as _fd:
        data = pyben.load(_fd)
    assert data is not None


def test_api_dump_iobuffer(tempmeta):
    """Test encoding to file."""
    meta, path = tempmeta
    with open(path, "wb") as _fd:
        pyben.dump(meta, _fd)
    assert os.path.exists(path)
    context.rmpath(path)


def test_dump_eq_load(tempmeta):
    """Test encoding inline then decoding."""
    meta, path = tempmeta
    pyben.dump(meta, path)
    assert meta["info"] == pyben.load(path)["info"]
    context.rmpath(path)


def test_pyben_excp3():
    """Test DecodeError Exception."""
    try:
        raise pyben.exceptions.DecodeError(b"000000|`")
    except pyben.exceptions.DecodeError:
        assert True


def test_pyben_excp2():
    """Test EncodeError Exception."""
    try:
        raise pyben.exceptions.EncodeError("000000|`")
    except pyben.exceptions.EncodeError:
        assert True


def test_pyben_excp1():
    """Test FilePathError Exception."""
    try:
        raise pyben.exceptions.FilePathError("somefile.torrent")
    except pyben.exceptions.FilePathError:
        assert True


def test_api_param_doesnt_exist():
    """Test load function with path argument that doesn't exist."""
    try:
        pyben.load("loremipsumunimjohnny")
    except pyben.exceptions.FilePathError:
        assert True


def test_api_param_none():
    """Test load function with None as path argument."""
    try:
        pyben.load(None)
    except pyben.exceptions.FilePathError:
        assert True


def test_api_load_json(tempfile):
    """Test api load function with optional json option set True."""
    jsonmeta = pyben.load(tempfile, to_json=True)
    assert json.dumps(jsonmeta) is not None


def test_api_loads_json(tempfile):
    """Test api loads function with json parameter active."""
    with open(tempfile, "rb") as binfile:
        data = binfile.read()
    jsonmeta = pyben.loads(data, to_json=True)
    assert json.dumps(jsonmeta) is not None


def test_api_show_dict(tempmeta):
    """Test show function with dictionary as input."""
    meta, _ = tempmeta
    assert pyben.show(meta)


def test_api_show_iobuffer(tempmeta):
    """Test show function with opened file buffer as input."""
    meta, path = tempmeta
    pyben.dump(meta, path)
    with open(path, "rb") as binfile:
        output = pyben.show(binfile)
    assert output
    context.rmpath(path)


def test_api_show_path(tempmeta):
    """Test show function with PathLike as input."""
    meta, path = tempmeta
    pyben.dump(meta, path)
    from pathlib import Path

    path = Path(path)
    assert pyben.show(path)
    context.rmpath(path)


def test_api_show_str():
    """Test show function with a string as input."""
    meta = "A Duck, quacked!"
    assert pyben.show(meta)


def test_api_show_bytes(tempmeta):
    """Test show function with bytes or bytearray as input."""
    meta, path = tempmeta
    pyben.dump(meta, path)
    with open(path, "rb") as binfile:
        meta = binfile.read()
    assert pyben.show(meta)
    context.rmpath(path)
