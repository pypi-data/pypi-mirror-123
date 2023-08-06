from tests.helpers.testbase import TestBase
from cerami.datatype import ByteBuffer
from cerami.datatype.translator import ByteTranslator

class TestByteTranslator(TestBase):
    def setUp(self):
        self.dt = ByteBuffer()
        self.translator = ByteTranslator(self.dt)

    def test_format_for_dynamodb(self):
        """it returns the value as a string"""
        assert self.translator.format_for_dynamodb('hello') == 'hello'.encode('utf-8')

    def test_format_for_cerami(self):
        """it returns the value an encoded"""
        assert self.translator.format_for_cerami('hello') == 'hello'.encode('utf-8')

