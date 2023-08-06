from tests.helpers.testbase import TestBase
from cerami.datatype import Number
from cerami.datatype.translator import DecimalTranslator
from decimal import Decimal

class TestDecimalTranslator(TestBase):
    def setUp(self):
        self.dt = Number()
        self.translator = DecimalTranslator(self.dt)

    def test_format_for_dynamodb(self):
        """it returns the value as a string"""
        assert self.translator.format_for_dynamodb(1) == '1'
        assert self.translator.format_for_dynamodb(123.456) == '123.456'

    def test_format_for_cerami(self):
        """it returns the value as a decimal"""
        assert self.translator.format_for_cerami('1') == Decimal('1')
        assert self.translator.format_for_cerami('123.456') == Decimal('123.456')
