from .base_datatype import DynamoDataType
from .translator import IntegerTranslator
from .expression import ArithmeticExpression

class BaseNumber(DynamoDataType):
    """A Base class for all Number datatypes
    
    By default, numbers are translated to integers. In order to including floating point
    precision, change the translator_cls to the DecimalTranslator
    """

    def __init__(self, translator_cls=IntegerTranslator, default=None, column_name=""):
        """constructor for the BaseNumber

        Parameters:
            default: a default value for the column. It can be a value or function
            column_name: a string defining the name of the column on the table
            translator_cls: A Translator class to manipulate data to/from dynamodb.
                Defaults to the IntegerTranslator. Use the DecimalTranslator for floats
        """
        super(BaseNumber, self).__init__(
            translator_cls=translator_cls,
            condition_type="N",
            default=default,
            column_name=column_name)

    def add(self, value):
        """add value to number for an UpdateRequest

        Parameters:
            value: a number to add

        Returns:
            An ArithmeticExpression

        For example::

            Person.update.key(Person.email == "test@test.com").set(Person.age.add(10))
        """
        return ArithmeticExpression('+', self, value)

    def subtract(self, value):
        """subtract value from number for an UpdateRequest

        Parameters:
            value: a number to subtract

        For example::

            Person.update \\
                .key(Person.email == "test@test.com") \\
                .set(Person.age.subtract(10))
        """
        return ArithmeticExpression('-', self, value)
