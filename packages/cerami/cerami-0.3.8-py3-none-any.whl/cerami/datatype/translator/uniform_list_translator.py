from .base_datatype_translator import BaseDatatypeTranslator

class UniformListTranslator(BaseDatatypeTranslator):
    """A Translator class for UniformLists

    Unlike the ListTranslator, the UniformListTranslatordoes not need to guess which
    datatype each item in the array is.

    For example::

        translator = UniformListTranslator(StringTranslator(String()))
        translator.to_dynamodb(["hello", "world"])
        {
            "L": [
                {
                    "S": "hello"
                },
                {
                    "S": "world"
                }
            ]
        }

        translator.to_cerami({"L": [{"S": "hello"}, {"S": "world"}]})
        ["hello", "world"]
    """

    def __init__(self, translator):
        """constructor for UniformListTranslator

        Parameters:
            translator: a BaseDatatypeTranslator object
        """
        self.translator = translator
        self.condition_type = "L"

    def format_for_dynamodb(self, value):
        return [self.translator.to_dynamodb(i) for i in value]

    def format_for_cerami(self, value):
        return [self.translator.to_cerami(i) for i in value]
