from .base_datatype_translator import BaseDatatypeTranslator

class IntegerTranslator(BaseDatatypeTranslator):
    """A Translator class for converting number fields into DynamoDB dictionaries

    It rounds down to convert any number into an integer

    For example::

        translator  = IntegerTranslator(Number())
        translator.to_dynamodb(30.6)
        {'N': '30'}

        translator.to_cerami({'N': '30'})
        30
    """
    def format_for_dynamodb(self, value):
        """convert the number into a string"""
        return str(int(value))

    def format_for_cerami(self, value):
        """convert the value into an int"""
        return int(value)

