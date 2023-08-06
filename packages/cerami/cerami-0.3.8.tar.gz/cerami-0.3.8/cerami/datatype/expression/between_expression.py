from .base_expression import BaseExpression

class BetweenExpression(BaseExpression):
    """A class to generate a `BETWEEN` expression for querying/scanning

    When using with a `QueryRequest`, a `BetweenExpression` can only be used on
    the sort key. It cannot be used on the partition key.

    For example::

        # You can use Person.age.between instead!
        expression = BetweenExpression(Person.age, 10, 20)
        Person.scan.filter(expression).build()
        {
           "TableName": "people",
           "FilterExpression": "#__age BETWEEN :_email_xfdww AND :_email_xcaf",
           "ExpressionAttributeNames": {
                "#__email": "email",
           },
           "ExpressionAttributeValues": {
                ":_email_xfdww": {
                    "N": 10,
                },
                ":_email_xcaf": {
                    "N": 20,
                },
           },
        }
    """
    def __init__(self, datatype, greater_than, less_than):
        super(BetweenExpression, self).__init__(
            'BETWEEN',
            datatype,
            [greater_than, less_than],
        )
        self.expression_attribute_values = self._build_expression_attribute_values()

    def __str__(self):
        value_names = ' AND '.join([k for k,v in self.value_dict().items()])
        attr_name = self.expression_attribute_name
        if hasattr(self.datatype, '_index'):
            attr_name = "{}[{}]".format(attr_name, self.datatype._index)
        return "{attr_name} {expression} {value_names}".format(
            attr_name=attr_name,
            expression=self.expression,
            value_names=value_names)

    def value_dict(self):
        """return the expected dict for expression-attribute-values

        This is used by many of different requests when building search_attributes. Most
        requests require the `ExpressionAttributeValue` option. This will build that
        corresponding property for this particular expression. Since the value
        is an array, this method overrides the ``BaseExpression`` implementation.

        Returns:
            a dict that can be used in ExpressionAttributeValue options
        """
        return self.expression_attribute_values

    def _build_expression_attribute_values(self):
        column_name_safe = self.datatype.column_name.replace('.', '_')
        res = {}
        for v in self.value:
            value_name = self._generate_variable_name(column_name_safe)
            value_mapped = self.datatype.translator.to_dynamodb(v)
            res[value_name] = value_mapped
        return res
