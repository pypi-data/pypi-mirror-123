from mock import patch
from tests.helpers.testbase import TestBase
from cerami.datatype import String
from cerami.datatype.expression import BetweenExpression

class TestBetweenExpression(TestBase):
    def setUp(self):
        self.dt = String(column_name="testcol")

    def test__init__(self):
        with patch('cerami.datatype.expression.BetweenExpression._build_expression_attribute_values') as build:
            build.return_value = 'mockedExpressionAttributeValues'
            expression = BetweenExpression(self.dt, 'a', 'c')
            assert expression.expression_attribute_values == 'mockedExpressionAttributeValues'

    def test_value_dict(self):
        with patch('cerami.datatype.expression.BetweenExpression._build_expression_attribute_values') as build:
            build.return_value = 'mockedExpressionAttributeValues'
            expression = BetweenExpression(self.dt, 'a', 'c')
            assert expression.value_dict() == 'mockedExpressionAttributeValues'

    def test__str__(self):
        """it returns the expected expression"""
        expression = BetweenExpression(self.dt, 'a', 'c')
        attr_name = expression.expression_attribute_name
        value_names = list(expression.value_dict().keys())
        expected = "{} BETWEEN {} AND {}".format(attr_name, value_names[0], value_names[1])
        assert str(expression) == expected

