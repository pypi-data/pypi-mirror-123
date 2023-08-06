from mock import patch, Mock
from tests.helpers.testbase import TestBase
from cerami.datatype import String
from cerami.datatype.translator import BaseDatatypeTranslator

class TestBaseDatatypeTranslator(TestBase):
    def setUp(self):
        self.dt = String()
        self.translator = BaseDatatypeTranslator(self.dt)

    def test_to_dynamodb_none(self):
        """it returns the NULL object when value is None"""
        assert self.translator.to_dynamodb(None) == {'NULL': True}

    def test_to_dynamodb(self):
        """it returns a dict
        with the key the condition_type
        and the value the result of resolve()
        """
        with patch('cerami.datatype.translator.BaseDatatypeTranslator.format_for_dynamodb') as resolve:
            resolve.return_value = "mocked"
            res = self.translator.to_dynamodb('test')
            assert res == {"S": "mocked"}

    def test_to_cerami_null(self):
        """it returns None when mapped_dict is NULL"""
        assert self.translator.to_cerami({'NULL': True}) == None

    def test_to_cerami_calls_format_for_cerami(self):
        """calls format_for_cerami when the value is not NULL"""
        self.translator.format_for_cerami = Mock()
        self.translator.to_cerami({'S': 'test'})
        self.translator.format_for_cerami.assert_called_with('test')

    def test_format_for_cerami(self):
        """returns the value"""
        assert self.translator.format_for_cerami('test') == 'test'
