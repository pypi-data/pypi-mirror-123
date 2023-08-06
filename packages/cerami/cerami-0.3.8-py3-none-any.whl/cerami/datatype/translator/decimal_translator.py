from decimal import Decimal
from .base_datatype_translator import BaseDatatypeTranslator

class DecimalTranslator(BaseDatatypeTranslator):
    """A Translator class for converting decimal number fields into DynaomDB dictionaries

    For example::

        translator = DecimalTranslator(Number())
        translator.to_dynamodb(30)
        {'N': '30'}

        translator.to_dynamodb(30.69213)
        {'N': '30.69213'}

        translator.to_cerami({'N': '30'})
        Decimal('30')

        translator.to_cerami({'N': '30.69213'})
        Decimal('30.69213')
    """
    def format_for_dynamodb(self, value):
        """convert the number into a decimal string"""
        return str(Decimal(str(value)))

    def format_for_cerami(self, value):
        """convert the value back into a Decimal"""
        return Decimal(value)
