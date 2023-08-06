from tests.helpers.testbase import TestBase
from cerami.datatype import Boolean
from cerami.datatype.translator import BooleanTranslator

class TestBooleanTranslator(TestBase):
    def setUp(self):
        self.dt = Boolean()
        self.translator = BooleanTranslator(self.dt)

    def test_format_for_dynamodb(self):
        assert self.translator.format_for_dynamodb(True) == True
        assert self.translator.format_for_dynamodb(False) == False

    def test_format_for_cerami(self):
        assert self.translator.format_for_dynamodb(True)
        assert not self.translator.format_for_dynamodb(False)

