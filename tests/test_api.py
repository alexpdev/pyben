import os
import pytest
import pyben
from tests import testfile, testmeta, rmpath


@pytest.fixture
def tempfile():
    fd = testfile()
    yield fd
    rmpath(fd)


@pytest.fixture
def tempmeta():
    parent = os.path.dirname(os.path.abspath(__file__))
    tfile = os.path.join(parent, "tempfile.pyben")
    meta = testmeta()
    return meta, tfile


@pytest.fixture
def encoded():
    meta = testmeta()


def test_api_loads():
    encoded = b"di1234el5:helloi99876eee"
    assert pyben.loads(encoded) == {1234: ["hello", 99876]}


def test_api_dumps():
    meta = {1234: ["hello", 99876]}
    assert pyben.dumps(meta) == b"di1234el5:helloi99876eee"


def test_api_loads_exists(tempfile):
    fd = tempfile
    assert os.path.exists(fd)


def test_api_loads_type(tempfile):
    decoded = pyben.load(tempfile)
    assert isinstance(decoded, dict)


def test_api_loads_containes(tempfile):
    decoded = pyben.load(tempfile)
    assert "ubuntu.com" in decoded["announce"].lower()


def test_api_dump_string(tempmeta):
    meta, path = tempmeta
    pyben.dump(meta, path)
    assert os.path.exists(path)
    rmpath(path)


def test_api_dump_iobuffer(tempmeta):
    meta, path = tempmeta
    pyben.dump(meta, open(path, "wb"))
    assert os.path.exists(path)
    rmpath(path)


def test_dump_eq_load(tempmeta):
    meta, path = tempmeta
    pyben.dump(meta, path)
    assert meta == pyben.load(path)
    rmpath(path)


def test_pyben_excp3():
    try:
        raise pyben.exceptions.DecodeError(b"000000|`")
    except pyben.exceptions.DecodeError:
        assert True

def test_pyben_excp2():
    try:
        raise pyben.exceptions.EncodeError("000000|`")
    except pyben.exceptions.EncodeError:
        assert True

def test_pyben_excp1():
    try:
        raise pyben.exceptions.FilePathError("somefile.torrent")
    except pyben.exceptions.FilePathError:
        assert True
