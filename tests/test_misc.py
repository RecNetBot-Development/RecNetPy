import pytest
from src.recnetpy.misc import stringify_bulk, date_to_unix, bitmask_decode

class TestStringifyBulk:
    def test_int_string_bool(self):
        result = stringify_bulk([42, "test", True])
        expected = ["42", "test", "True"]
        assert result == expected
    
    def test_empty_list(self):
        result = stringify_bulk([])
        expected = []
        assert result == expected

class TestDateToUnix:
    def test_ISO_8601(self):
        result = date_to_unix("2024-06-10T00:00:00+00:00")
        expected = 1717977600
        assert result == expected

    def test_invalid(self):
        with pytest.raises(ValueError) as e_info:
            date_to_unix("invalid")

class TestBitmaskDecode:
    def test_valid(self):
        result = bitmask_decode(1, ["test", "test2"])
        expected = ["test"]
        assert result == expected

    def test_empty_list(self):
        result = bitmask_decode(1, [])
        expected = []
        assert result == expected

