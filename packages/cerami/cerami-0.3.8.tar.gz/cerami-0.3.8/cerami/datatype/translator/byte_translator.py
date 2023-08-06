from .base_datatype_translator import BaseDatatypeTranslator

class ByteTranslator(BaseDatatypeTranslator):
    """A Translator class for byte encoding data

    This translator  is typically used with the ByteBuffer datatype. This class will
    automatically encode the value passed.

    For example::

         translator  = ByteTranslator(DynamoDataType(condition_type="B"))
         # You can pass a string if you wanted to for example
         translator.to_dynamodb("hello world")
         {'B': b'hello world'}

         # But the string will not be returned when reconstructing
         translator.to_cerami({'B': b'hello world'})
         b'helo world'
    """
    def format_for_dynamodb(self, value):
        """UTF-8 encode the value

        Parameters:
            value: a string to be encoded or an already encoded stream.

        Returns:
            a UTF-8 encoded version of value. If the value fails to be utf-8 encoded, it
            will return the value as-is
        """
        return self._encode(value)

    def format_for_cerami(self, value):
        """UTF-8 encode the value

        Parameters:
            value: a string to be encoded or an already encoded stream.

        Returns:
            a UTF-8 encoded version of value. If the value fails to be utf-8 encoded, it
            will return the value as-is
        """
        return self._encode(value)

    def _encode(self, value):
        """try to encode it or return the value (meaning its already encoded"""
        try:
            return value.encode('utf-8')
        except AttributeError:
            return value
