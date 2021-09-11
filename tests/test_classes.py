
from benencode import Bendecoder, Benencoder
from tests import TestBase


class TestBendecoder(TestBase):
    def test_decode_str(self):
        decoder = Bendecoder()
        for string, benstring in self.strings:
            text, feed = decoder._decode_str(benstring)
            assert string == text
            assert feed == len(benstring)

    def test_decode_int(self):
        decoder = Bendecoder()
        for num, benint in self.ints:
            real, feed = decoder._decode_int(benint)
            assert real == num
            assert feed == len(benint)

    def test_decode_list(self):
        decoder = Bendecoder()
        for lst, benlist in self.lists:
            decoded, _ = decoder._decode_list(benlist)
            assert decoded == lst

    def test_decode_dict(self):
        decoder = Bendecoder()
        for dct, bendict in self.dicts:
            decoded, _ = decoder._decode_dict(bendict)
            assert dct == decoded

    def test_decode(self):
        decoder = Bendecoder()
        for data in self.data:
            for item, benitem in data:
                decoded = decoder.decode(benitem)
                assert decoded == item


class TestBencoder(TestBase):
    def test_bencode_str(self):
        encoder = Benencoder()
        for string, benstring in self.strings:
            text = encoder._encode_str(string)
            assert benstring == text

    def test_bencode_int(self):
        encoder = Benencoder()
        for num, benint in self.ints:
            real = encoder._encode_int(num)
            assert real == benint

    def test_bencode_list(self):
        encoder = Benencoder()
        for lst, benlist in self.lists:
            encoded = encoder._encode_list(lst)
            assert encoded == benlist

    def test_decode_dict(self):
        encoder = Benencoder()
        for dct, bendict in self.dicts:
            encoded = encoder._encode_dict(dct)
            assert bendict == encoded

    def test_decode(self):
        encoder = Benencoder()
        for data in self.data:
            for item, benitem in data:
                encoded = encoder.encode(item)
                assert encoded == benitem
