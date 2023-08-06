from mock import patch, Mock, call
from tests.helpers.testbase import TestBase
from cerami.datatype import String
from cerami.datatype.translator import (
    BaseDatatypeTranslator,
    SetTranslator)

class TestSetMapper(TestBase):
    def setUp(self):
        self.dt = String()
        self.translator = BaseDatatypeTranslator(self.dt)
        self.translator.condition_type = 'S'
        self.decorator = SetTranslator(self.translator)

    def test__init__(self):
        assert self.decorator.translator == self.translator

    def test_to_dynamodb(self):
        with patch("cerami.datatype.translator.SetTranslator.format_for_dynamodb") as resolve:
            resolve.return_value = 'mocked'
            res = self.decorator.to_dynamodb(['test'])
            assert res == {"SS": "mocked"}

    def test_format_for_dynamodb(self):
        """it calls translator.format_for_dynamodb for each item in value"""
        self.decorator.translator = Mock()
        self.decorator.translator.format_for_dynamodb.return_value = "mocked"
        calls = [call(1), call(2)]
        res = self.decorator.format_for_dynamodb([1,2])
        assert res == ['mocked', 'mocked']
        self.decorator.translator.format_for_dynamodb.assert_has_calls(calls)

    def test_format_for_cerami(self):
        """assigns the value directly from mapped_dict"""
        value = ['zac', 'test']
        assert self.decorator.format_for_cerami(value) == ['zac', 'test']
