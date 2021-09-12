import os
import shutil
from tests.testdata import ints, strings, dicts, lists, data
from pyben import bencode

__all__ = ["lists", "strings", "dicts", "ints", "data"]


def rmpath(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    return


def testmeta():
    meta = {
        "announce": "http://ubuntu.com/announce",
        "info": {
            "name": "ubuntu.iso",
            "length": 12845738,
            "piece length": 262144,
            "private": 1,
            "source": "ubuntu",
        },
        "created by": "mktorrent",
    }
    return meta


def testfile():
    parent = os.path.dirname(os.path.abspath(__file__))
    tfile = os.path.join(parent, "tempfile.pyben")
    meta = testmeta()
    with open(tfile, "wb") as fd:
        encoded = bencode.benencode(meta)
        fd.write(encoded)
    return tfile
