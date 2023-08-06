from .base_datatype_translator import BaseDatatypeTranslator

class SetTranslator(BaseDatatypeTranslator):
    """A Translator class for converting a Set into a DynamoDB dictionary

    For example::

        translator = SetTranslator(StringTranslator(String()))
        translator.to_dynamodb(["hello", "world"])
        {'SS': ['hello', 'world']}

        translator.to_cerami({'SS': ['hello', 'world']})
        ['hello', 'world']
    """
    def __init__(self, translator):
        """constructor for SetTranslator

        Parameters:
           translator: a Translator object that this Set decoratar shall wrap 
        """
        self.translator = translator
        self.condition_type = self.translator.datatype.condition_type + "S"

    def format_for_dynamodb(self, value):
        return [self.translator.format_for_dynamodb(i) for i in value]

    def format_for_cerami(self, value):
        return [self.translator.format_for_cerami(i) for i in value]
