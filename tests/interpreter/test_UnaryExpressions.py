import re

import pytest

from nyr.interpreter.interpreter import Interpreter
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("operator"), (
		("-"),
		("+"),
		("!"),
	),
)
def testUnaryNone(operator: str):
	ast = Parser().parse(f"let x = {operator}null;")

	with pytest.raises(Exception, match=re.escape(f'Cannot use {operator} on "null"')):
		Interpreter().interpret(ast)


@pytest.mark.parametrize(
	("operator"), (
		("-"),
		("+"),
	),
)
def testUnaryInteger(operator: str):
	ast = Parser().parse(f"let x = {operator}5;")
	env = Interpreter().interpret(ast)

	if operator == "+":
		assert env == {"x": 5}
	else:
		assert env == {"x": -5}


@pytest.mark.parametrize(
	("boolValue"), (
		("true"),
		("false"),
	),
)
def testUnaryNotBool(boolValue: str):
	ast = Parser().parse(f"let x = !{boolValue};")
	env = Interpreter().interpret(ast)

	assert env == {"x": boolValue != "true"}
