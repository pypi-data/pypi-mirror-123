from .base_datatype_translator import BaseDatatypeTranslator

class ModelTranslator(BaseDatatypeTranslator):
    """A Translator class for converting Models to DynamoDB dictionaries

    The ModelTranslator must be initialized with a ModelMap datatype. It depends on the
    model_cls attribute to know which columns and datatypes to use.

    The benefit of using a ModelTranslator over a DictMapper is there is no guess work.
    Because all columns are defined, it automatically knows the datatypes to use.

    For example::

        child = Child(gender="female", age=2)
        translator = ModelTranslator(ModelMap(model_cls=Child))
        translator.to_dynamodb(child)
        {
            "M": {
                "gender": {
                    "S": "female"
                },
                "age": {
                    "N": "2"
                },
                "name": {
                    "NULL": True,
                },
            }
        }

        translator.to_cerami({"M": {"name": {"S": "Baby"}}})
        <Child object>
    """

    def format_for_dynamodb(self, value):
        """Convert the model into a DynamoDB formatted dictionary

        Any values column values that are not set on the instance being translated  will
        automatically set the ``{"NULL": True}`` for that column

        Parameters:
            value: the model to be converted

        Returns:
            a dictionary where each key is a column of the model and the value is the
            translated version of the column value
        """
        res = {}
        model_cls = self.datatype.model_cls
        for column in model_cls._columns:
            column_datatype = getattr(model_cls, column.column_name)
            column_value = getattr(value, column.column_name, None)
            res[column.column_name] = column_datatype.translator.to_dynamodb(column_value)
        return res

    def format_for_cerami(self, value):
        """Convert the DynamoDB dict into an instance of the model

        Iterate over all columns on the Model. Use the columns translate the value.

        Parameters:
            value: a dictionary where each key represents a column of the model as a 
                DynamoDB formatted dictionary

        Returns:
            an instance of the model class
        """
        data = {}
        model_cls = self.datatype.model_cls
        for column in model_cls._columns:
            try:
                val = value[column.column_name]
            except KeyError:
                continue
            data[column.column_name] = column.translator.to_cerami(val)
        return model_cls(**data)
