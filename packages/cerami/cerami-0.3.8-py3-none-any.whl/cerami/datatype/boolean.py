from .base_datatype import DynamoDataType
from .translator.boolean_translator import BooleanTranslator

class Boolean(DynamoDataType):
    """A class for Boolean datatypes"""

    def __init__(self, translator_cls=BooleanTranslator, default=None, column_name=""):
        """constructor for the Boolean datatype

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            translator_cls: A translator class to manipulate data to/from dynamodb.
                Defaults to the BooleanTranslator
        """
        super(Boolean, self).__init__(
            translator_cls=translator_cls,
            condition_type="BOOL",
            default=default,
            column_name=column_name)
