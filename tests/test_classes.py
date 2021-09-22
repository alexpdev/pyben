import os
import pytest
from pyben.classes import Bendecoder, Benencoder
from tests import data, testfile, rmpath, testmeta

# tfile={
# "announce": "http://ubuntu.com/announce",
# "info": {
#  "name": "ubuntu.iso",
#  "length": 12845738,
#  "piece length": 262144,
#  "private": 1,
#  "source": "ubuntu",
# },
# "created by": "mktorrent",
# }

@pytest.fixture
def tfile():
    tempfile = testfile()
    yield tempfile
    rmpath(tempfile)

@pytest.fixture
def tmeta():
    info = testmeta()
    return info


@pytest.fixture
def ints():
    nums = data[0]
    return nums


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


def test_decode_str(strings):
    decoder = Bendecoder()
    for string, benstring in strings:
        text, feed = decoder._decode_str(benstring)
        assert string == text
        assert feed == len(benstring)


def test_decode_int_class(ints):
    decoder = Bendecoder()
    for num, benint in ints:
        real, feed = decoder._decode_int(benint)
        assert real == num
        assert feed == len(benint)


def test_decode_list_class(lists):
    decoder = Bendecoder()
    for lst, benlist in lists:
        decoded, _ = decoder._decode_list(benlist)
        assert decoded == lst


def test_decode_dict_class(dicts):
    decoder = Bendecoder()
    for dct, bendict in dicts:
        decoded, _ = decoder._decode_dict(bendict)
        assert dct == decoded


def test_decode_class(tdata):
    decoder = Bendecoder()
    for val in tdata:
        for item, benitem in val:
            decoded = decoder.decode(benitem)
            assert decoded == item

def test_decode_load(tfile):
    decoder = Bendecoder()
    output = decoder.load(tfile)
    assert isinstance(output, dict)

def test_decode_loads(tfile):
    inp = open(tfile,"rb").read()
    decoder = Bendecoder()
    out = decoder.loads(inp)
    assert out["info"]["length"] == 12845738


def test_bencode_str(strings):
    encoder = Benencoder()
    for string, benstring in strings:
        text = encoder._encode_str(string)
        assert benstring == text


def test_bencode_int(ints):
    encoder = Benencoder()
    for num, benint in ints:
        real = encoder._encode_int(num)
        assert real == benint


def test_bencode_list(lists):
    encoder = Benencoder()
    for lst, benlist in lists:
        encoded = encoder._encode_list(lst)
        assert encoded == benlist

def test_bencode_dump(tmeta, tfile):
    encoder = Benencoder()
    encoder.dump(tmeta, tfile)
    assert os.path.exists(tfile)

def test_bencode_dumps(tmeta):
    encoder = Benencoder()
    reg = encoder.dumps(tmeta)
    assert isinstance(reg, bytes)


def test_decode_dict(dicts):
    encoder = Benencoder()
    for dct, bendict in dicts:
        encoded = encoder._encode_dict(dct)
        assert bendict == encoded


def test_decode(tdata):
    encoder = Benencoder()
    for val in tdata:
        for item, benitem in val:
            encoded = encoder.encode(item)
            assert encoded == benitem
