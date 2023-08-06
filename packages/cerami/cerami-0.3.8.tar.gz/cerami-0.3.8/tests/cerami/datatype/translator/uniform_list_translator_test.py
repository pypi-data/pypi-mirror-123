from mock import Mock
from tests.helpers.testbase import TestBase
from cerami.datatype.translator import UniformListTranslator


class TestUniformListMapper(TestBase):
    def setUp(self):
        self.mocked_translator = Mock()
        self.translator = UniformListTranslator(self.mocked_translator)

    def test__init__(self):
        """it sets translator"""
        assert self.translator.translator == self.mocked_translator

    def test_to_dynamodb(self):
        """it calls mocked_translator for each item in the list and returns the dict"""
        self.mocked_translator.to_dynamodb.return_value = 'mocked'
        val = [1]
        assert self.translator.to_dynamodb(val) == {'L': ['mocked']}
        self.mocked_translator.to_dynamodb.assert_called_with(1)

    def test_format_for_dynamodb(self):
        """it calls mocked_translator for each value"""
        self.mocked_translator.to_dynamodb.return_value = 'mocked'
        val = [1]
        assert self.translator.format_for_dynamodb(val) == ['mocked']
        self.mocked_translator.to_dynamodb.assert_called_with(1)

    def test_format_for_cerami(self):
        """it calls translator.to_cerami for each item in the list"""
        self.mocked_translator.to_cerami.return_value = 'mocked'
        value = [{'S': 'test'}]
        assert self.translator.format_for_cerami(value) == ['mocked']
        self.mocked_translator.to_cerami.assert_called_with({'S': 'test'})
