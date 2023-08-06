from mock import patch, Mock
from tests.helpers.testbase import TestBase
from cerami.datatype import Set, String
from cerami.datatype.expression import ContainsExpression

class TestContainsExpression(TestBase):
    def setUp(self):
        self.dt = String(column_name="testcol")
        self.set_dt = Set(String(), column_name="settest")
        with patch('cerami.datatype.expression.BaseExpression._generate_variable_name') as gen:
            gen.return_value = "mocked"
            self.expression = ContainsExpression(self.dt, "test")
            self.set_expression = ContainsExpression(self.set_dt, "test", is_set=True)
            #self.expression = BaseExpression('=', self.dt, 'test')

    def test__str__(self):
        expected_string = "contains(#__testcol, mocked)"
        expected_set = "contains(#__settest, mocked)"
        assert self.expression.__str__() == expected_string
        assert self.set_expression.__str__() == expected_set

    def test_set_value_dict(self):
        """it uses the set's inner datatype to build the contains value_dict"""
        expected = { "mocked": { "S":  "test" } }
        assert self.set_expression.value_dict() == expected

    def test_value_dict(self):
        """it uses the BaseExpression's value_dict when the datatype is not a set"""
        expected = { "mocked": { "S": "test" } }
        assert self.expression.value_dict() == expected

