from .base_datatype_translator import BaseDatatypeTranslator

class StringTranslator(BaseDatatypeTranslator):
    """A Translator class for converting string fields into DynamoDB strings

    For example::

        translator = StringTranslator(String())
        translator.to_dynamodb("hello world")
        {'S': "hello world"}

        translator.to_cerami({'S': "hello world"})
        "hello world"
    """
    
    def format_for_dynamodb(self, value):
        return str(value)

    def format_for_cerami(self, value):
        return str(value)
