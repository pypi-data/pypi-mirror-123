from tests.helpers.testbase import TestBase
from cerami.datatype import Number
from cerami.datatype.translator import IntegerTranslator

class TestIntegerTranslator(TestBase):
    def setUp(self):
        self.dt = Number()
        self.translator = IntegerTranslator(self.dt)

    def test_format_for_dynamodb(self):
        """it returns the value as a string"""
        assert self.translator.format_for_dynamodb(1) == '1'

    def test_format_for_cerami(self):
        """it returns the value as an int"""
        assert self.translator.format_for_cerami('1') == 1
