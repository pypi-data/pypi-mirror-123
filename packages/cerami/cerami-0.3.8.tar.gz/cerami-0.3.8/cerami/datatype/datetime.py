import dateutil.parser
from datetime import datetime, timezone
from .base_string import BaseString
from .translator import DatetimeTranslator

class Datetime(BaseString):
    """A class to represent all Datetime datatypes"""

    def __init__(self, translator_cls=DatetimeTranslator, default=None, column_name=""):
        """constructor for the Datetime

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            translator_cls: A Translator class to manipulate data to/from dynamodb.
                Defaults to the DatetimeTranslator
        """
        super(Datetime, self).__init__(
            translator_cls=translator_cls,
            default=default,
            column_name=column_name)
