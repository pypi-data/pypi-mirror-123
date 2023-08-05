from unittest import TestCase

from ..code import error_dict, success_dict


class CodeTest(TestCase):
    def test_response(self):
        assert "code" in error_dict("test")
        assert "code" in success_dict("test", {})
