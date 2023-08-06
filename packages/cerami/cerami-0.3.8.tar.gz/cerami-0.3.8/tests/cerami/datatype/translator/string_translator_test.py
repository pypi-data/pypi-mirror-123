from tests.helpers.testbase import TestBase
from cerami.datatype import String
from cerami.datatype.translator import StringTranslator

class TestStringTranslator(TestBase):
    def setUp(self):
        self.dt = String()
        self.translator = StringTranslator(self.dt)

    def test_format_for_dynamodb(self):
        """it returns the value as a string"""
        assert self.translator.format_for_dynamodb(1) == "1"
