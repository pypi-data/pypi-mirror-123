from .base_datatype_translator import BaseDatatypeTranslator

class BooleanTranslator(BaseDatatypeTranslator):
    """A Translator class for converting fields into DynamoDB booleans

    For example::
    
        translator = BooleanTranslator(Boolean())
        translator.to_dynamodb(True)
        {'BOOL': True}

        translator.to_cerami({'BOOL': True})
        True
    """

    def format_for_dynamodb(self, value):
        return bool(value)

    def format_for_cerami(self, value):
        return bool(value)
