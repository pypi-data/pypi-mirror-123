from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.datatype import String, Map
from cerami.datatype.translator import (
    DictTranslator)

class TestDictTranslator(TestBase):
    def setUp(self):
        self.mocked_map_guesser = Mock()
        self.mocked_parse_guesser = Mock()
        self.dt = Map()
        self.translator = DictTranslator(
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
        val = {'test': 1}
        res = self.translator.format_for_dynamodb(val)
        assert res == {'test': 'mocked'}
        self.mocked_map_guesser.guess.assert_called_with('test', 1)
        mocked_dt.translator.to_dynamodb.assert_called_with(1)

    def test_format_for_cerami(self):
        """it uses guesser to find the correct datatype
        based on the value and calls to_cerami for that datatype
        """
        mocked_dt = Mock()
        mocked_dt.translator.to_cerami.return_value = "mocked"
        self.mocked_parse_guesser.guess.return_value = mocked_dt
        mapped_dict = {'M': {'testkey': {'S': 'testval'}}}
        assert self.translator.to_cerami(mapped_dict) == {'testkey': 'mocked'}
        self.mocked_parse_guesser.guess.assert_called_with(
            'testkey',
            {'S': 'testval'})
        mocked_dt.translator.to_cerami.assert_called_with({'S': 'testval'})
