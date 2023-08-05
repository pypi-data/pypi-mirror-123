import pytest
from django.test import Client

from .. import test
from ..code import Code


def test_assert_instance():
    test_data = "test"
    test.assert_instance(test_data, str)
    with pytest.raises(AssertionError):
        test.assert_instance(test_data, int)


def test_dict_has_key():
    key = "purchase_category"
    got = {"purchase_category": "test"}
    test.assert_key(key, got)
    key1 = "purchase"
    with pytest.raises(AssertionError):
        test.assert_key(key1, got)


def test_object_has_attr():
    keys = ("SUCCESS", "FAILED")
    test.assert_attr(Code, keys)
    case2 = ("FALSE", "test")
    with pytest.raises(AssertionError):
        test.assert_attr(Code, case2)


def test_assert_response_get():
    with pytest.raises(AssertionError):
        test.assert_response_get(Client(), "/test")


def test_export_file_type_and_details():
    data = {"test": "test"}
    resp = Client().get("/test", data)
    with pytest.raises(AssertionError):
        test.assert_export_file_type(resp)
        test.assert_export_file_details(resp, "test")


def test_assert_keys():
    data = {"code": 1, "msg": "success", "data": "hello"}

    keys = ("code", "msg", "data")
    test.assert_keys(keys, data)

    keys = ("test", "msg")
    with pytest.raises(AssertionError):
        test.assert_keys(keys, data)


def test_assert_equal():
    a, b = 1, 2
    with pytest.raises(AssertionError):
        test.assert_equal(a, b)

    a, b = 1, 1
    test.assert_equal(a, b)


def test_assert_structure():
    with pytest.raises(AssertionError):
        test.assert_response(Client(), "/test")

    with pytest.raises(AssertionError):
        test.assert_response(Client(), "/test", data={})


def test_utils_assert_in():
    data = {"code": 0, "msg": 1, "data": {"hello": "world"}}
    test.assert_response_format(data)

    with pytest.raises(AssertionError):
        data.pop("code")
        test.assert_response_format(data)


def test_utils_success():
    data = {"code": -1, "msg": 1, "data": {"hello": "world"}}

    with pytest.raises(ValueError):
        test.assert_code(data, Code.SUCCESS)

    data = {"code": 1, "msg": 1, "data": {"hello": "world"}}
    test.assert_code(data, Code.SUCCESS)


def test_assert_key_value():
    data = {"page": 1, "count": 2, "groups": []}

    keys = ("page", "count", "groups")
    value_types = (int, int, list)
    test.assert_key_value_types(data, keys, value_types)

    with pytest.raises(AssertionError):
        value_types = value_types[1:]
        test.assert_key_value_types(data, keys, value_types)
