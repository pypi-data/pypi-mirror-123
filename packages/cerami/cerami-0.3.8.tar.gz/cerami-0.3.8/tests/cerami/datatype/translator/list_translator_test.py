from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.datatype import String, List
from cerami.datatype.translator import (
    ListTranslator)

class TestListTranslator(TestBase):
    def setUp(self):
        self.mocked_map_guesser = Mock()
        self.mocked_parse_guesser = Mock()
        self.dt = List()
        self.translator = ListTranslator(
            self.dt,
            self.mocked_map_guesser,
            self.mocked_parse_guesser)

    def test__init__(self):
        """it sets guesser"""
        assert self.translator.map_guesser == self.mocked_map_guesser
        assert self.translator.parse_guesser == self.mocked_parse_guesser

    def test_format_for_dynamodb(self):
        """it uses guesser to find the correct datatype
        based on the value and calls to_dynamodb for that datatype
        """
        mocked_dt = Mock()
        mocked_dt.translator.to_dynamodb.return_value = "mocked"
        self.mocked_map_guesser.guess.return_value = mocked_dt
        val = ['test']
        res = self.translator.format_for_dynamodb(val)
        assert res == ['mocked']
        self.mocked_map_guesser.guess.assert_called_with(0, 'test')
        mocked_dt.translator.to_dynamodb.assert_called_with('test')

    def test_to_dynamodb(self):
        """it uses the guesser to find the correct datatype
        and returns a dict with the mapped value
        """
        mocked_dt = Mock()
        mocked_dt.translator.to_dynamodb.return_value = "mocked"
        self.mocked_map_guesser.guess.return_value = mocked_dt
        val = ['test']
        res = self.translator.to_dynamodb(val)
        assert res == {'L': ['mocked']}
        self.mocked_map_guesser.guess.assert_called_with(0, 'test')
        mocked_dt.translator.to_dynamodb.assert_called_with('test')

    def test_format_for_cerami(self):
        """it uses guesser to find the correct datatype
        based on the value and calls to_cerami for that datatype
        """
        mocked_dt = Mock()
        mocked_dt.translator.to_cerami.return_value = "mocked"
        self.mocked_parse_guesser.guess.return_value = mocked_dt
        value = [{'S': 'testval'}]
        assert self.translator.format_for_cerami(value) == ['mocked']
        self.mocked_parse_guesser.guess.assert_called_with(
            0,
            {'S': 'testval'})
        mocked_dt.translator.to_cerami.assert_called_with({'S': 'testval'})
