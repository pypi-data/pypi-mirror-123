class BaseDatatypeTranslator(object):
    """The base class for all Translators

    Translators are responsible for translating between a model's data and DynamoDB. All
    requests need to have the data formatted in a specific way, and all responses from
    DynamoDB are formatted similarly. A Translatoris responsible for converting to and
    from this DynamoDB structure.

    Attributes:
        datatype: a DynamoDataType object the translator is used with
        condition_type: The condition_type of the datatype. It defines in DynamoDB the
            type of key used in the dictionary ("N", "M", "S", ...)

    For example::

        translator = BaseDatatypeTranslator(Person.email)
        translator.to_dynamodb("test@test.com")
        {
            "S": "test@test.com"
        }

        translator.to_cerami({"S": "test@test.com"})
        "test@test.com"
    """
    def __init__(self, datatype):
        """constructor for the BaseDatatypeTranslator

        Parameters:
            datatype: a DynamoDataType object the translator is used with
        """
        self.datatype = datatype
        self.condition_type = self.datatype.condition_type

    def to_dynamodb(self, value):
        """return the value and its condition_type in the DynamoDB dict format

        Translating is done when converting the model into a form
        readable by DynamoDB. It involves two steps.
        First it must return a dict of the value.
        Second it must convert the value using the format_for_dynamodb() method

        Parameters:
            value: anything that should be converted into a DynamoDB formatted dict

        Returns:
            a dict in a format expected by DynamoDB. Its key is the condition_type of this
            instance and value the return value of ``format_for_dynamodb()``. It will
            automatically return ``{"NULL": True}`` when the value passed in is ``None``

        For example::

            translator = BaseDatatypeTranslator(Person.email)
            translator.to_dynamodb("test@test.com")
            {
                "S": "test@test.com"
            }
        """
        if value == None:
            return {'NULL': True}
        res = {}
        res[self.condition_type] = self.format_for_dynamodb(value)
        return res

    def format_for_dynamodb(self, value):
        """returns the value formatted for dynamodb

        This method is called by ``to_dynamodb()`` to convert the value
        itself into a format that is expected for DynamoDB. For example, all Number
        datatypes need to be converted to strings in before being submitted.

        Parameters:
            value: anything. It is the actual value that is submitted to DynamoDB

        Returns:
            the value as is. Any child class should override this method to convert the
            value as necessary.
        """
        return value

    def to_cerami(self, dynamodb_dict):
        """return the value from the DynamoDB dict for model instantiation

        DynamoDB returns all attributes as a dict. Reconstructing reads this dict and
        parses the value. The return value can be used as the attribute on the Model.
        Reconstructing is only responsible for parsing the data as-is from DynamoDB. The
        process of assigning default values is done by the datatype itself.

        Parameters:
            dynaomdb_dict: A DynamoDB dictionary, whose key is the condition type of this
                instance and value is what needs to be `parsed`. The key can also be
                ``"NULL"`` which represents null values in DynamoDB

        Returns:
            the parsed value from the `dynamodb_dict`. It will return ``None`` when
            the key of the dynamodb_dict is ``"NULL"``.

        For example::

            translator = BaseDatatypeTranslator(Person.email)
            translator.to_cerami({"S": "test@test.com"})
            "test@test.com"
        """
        if dynamodb_dict.get('NULL') == True:
            return None
        return self.format_for_cerami(dynamodb_dict[self.condition_type])

    def format_for_cerami(self, value):
        """Convert the value from DynamoDB into a format for the Model

        Parameters:
            value: anything that should be converted from a DynamoDB dict's value
                value should never be None, reconstruct will not pass it here
        Returns:
            the value as is. All child classes should override this method to convert the
            value however necessary.
        """
        return value
