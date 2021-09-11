from tests.test_data import ints, strings, dicts, lists, data


class TestBase:
    strings = strings
    ints = ints
    dicts = dicts
    lists = lists
    data = data


__all__ = ["lists", "strings", "dicts", "ints", "TestBase"]
