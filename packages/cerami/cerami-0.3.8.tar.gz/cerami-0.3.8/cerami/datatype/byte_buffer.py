from .base_datatype import DynamoDataType
from .translator import ByteTranslator

class ByteBuffer(DynamoDataType):
    """A class for all ByteBuffer and Binary datatypes"""

    def __init__(self, translator_cls=ByteTranslator, default=None, column_name=""):
        """constructor for the ByteBuffer

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            translator_cls: a translator class to manipulate data to/from dynamodb.
                Defaults to the ByteTranslator
        """
        super(ByteBuffer, self).__init__(
            translator_cls=translator_cls,
            condition_type="B",
            default=default,
            column_name=column_name)
