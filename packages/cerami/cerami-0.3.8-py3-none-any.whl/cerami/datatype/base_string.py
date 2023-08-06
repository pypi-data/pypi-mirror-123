from .base_datatype import DynamoDataType
from .expression import (
    ContainsExpression,
    BeginsWithExpression)
from .translator import StringTranslator

class BaseString(DynamoDataType):
    """A Base class for all String datatypes"""

    def __init__(self, translator_cls=StringTranslator, default=None, column_name=""):
        """constructor for the BaseString

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            translator_cls: A translator class to manipulate data to/from dynamodb.
                Defaults to the StringTranslator
        """
        super(BaseString, self).__init__(
            translator_cls=translator_cls,
            condition_type="S",
            default=default,
            column_name=column_name)

    def begins_with(self, value):
        """Build a BeginsWithExpression

        Can be used in Filters or KeyConditionExpressions to create a begins_with
        expression.

        Parameters:
            value: a substring to check if the column begins with

        Returns:
            A BeginsWithExpression

        For example::

            Person.scan.filter(Person.name.begins_with("Mo"))
        """
        return BeginsWithExpression(self, value)

    def contains(self, value):
        """Build a ContainsExpression

        Can be used in Filters only, cannot be part of a KeyConditionExpression

        Parameters:
            value: the value to filter upon

        Returns:
            A ContainsExpression

        For example::

            Person.scan.filter(Person.name.contains("om"))
        """
        return ContainsExpression(self, value)
