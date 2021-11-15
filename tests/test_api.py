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

import os

import pytest

import pyben

from . import context


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
    assert not os.path.exists("rmpath_test_file")  # nosec


def test_api_tuple_to_list():
    """Test encoding tuple to list."""
    lst = (130, "foobar", "foo:bar")
    assert pyben.dumps(lst) == b"li130e6:foobar7:foo:bare"  # nosec


@pytest.mark.parametrize("decoded, encoded", context.data())
def test_api_loads(decoded, encoded):
    """Test decoding inline."""
    assert pyben.loads(encoded) == decoded  # nosec


@pytest.mark.parametrize("decoded, encoded", context.data())
def test_api_dumps(decoded, encoded):
    """Test encoding inline."""
    assert pyben.dumps(decoded) == encoded  # nosec


def test_api_loads_exists(tempfile):
    """Test decoding from file."""
    fd = tempfile
    assert os.path.exists(fd)  # nosec


def test_api_loads_type(tempfile):
    """Test inline encoding type."""
    decoded = pyben.load(tempfile)
    assert isinstance(decoded, dict)  # nosec


def test_api_loads_containes(tempfile):
    """Test inline decoding containers."""
    decoded = pyben.load(tempfile)
    assert "ubuntu.com" in decoded["announce"].lower()  # nosec


def test_api_dump_string(tempmeta):
    """Test encoding to file."""
    meta, path = tempmeta
    pyben.dump(meta, path)
    assert os.path.exists(path)  # nosec
    context.rmpath(path)


def test_api_with_file_load(tempfile):
    """Test load function with opened BytesIO."""
    with open(tempfile, "rb") as _fd:
        data = pyben.load(_fd)
    assert data is not None  # nosec


def test_api_dump_iobuffer(tempmeta):
    """Test encoding to file."""
    meta, path = tempmeta
    with open(path, "wb") as _fd:
        pyben.dump(meta, _fd)
    assert os.path.exists(path)  # nosec
    context.rmpath(path)


def test_dump_eq_load(tempmeta):
    """Test encoding inline then decoding."""
    meta, path = tempmeta
    pyben.dump(meta, path)
    assert meta["info"] == pyben.load(path)["info"]  # nosec
    context.rmpath(path)


def test_pyben_excp3():
    """Test DecodeError Exception."""
    try:
        raise pyben.exceptions.DecodeError(b"000000|`")
    except pyben.exceptions.DecodeError:
        assert True  # nosec


def test_pyben_excp2():
    """Test EncodeError Exception."""
    try:
        raise pyben.exceptions.EncodeError("000000|`")
    except pyben.exceptions.EncodeError:
        assert True  # nosec


def test_pyben_excp1():
    """Test FilePathError Exception."""
    try:
        raise pyben.exceptions.FilePathError("somefile.torrent")
    except pyben.exceptions.FilePathError:
        assert True  # nosec


def test_api_param_doesnt_exist():
    """Test load function with path argument that doesn't exist."""
    try:
        pyben.load("loremipsumunimjohnny")
    except pyben.exceptions.FilePathError:
        assert True  # nosec


def test_api_param_none():
    """Test load function with None as path argument."""
    try:
        pyben.load(None)
    except pyben.exceptions.FilePathError:
        assert True  # nosec
