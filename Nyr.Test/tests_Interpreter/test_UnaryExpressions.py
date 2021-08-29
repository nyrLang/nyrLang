import re

import pytest

from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


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
		Interpreter(ast).interpret()


@pytest.mark.parametrize(
	("operator"), (
		("-"),
		("+"),
	),
)
def testUnaryInteger(operator: str):
	ast = Parser().parse(f"let x = {operator}5;")
	env = Interpreter(ast).interpret()

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
	env = Interpreter(ast).interpret()

	assert env == {"x": boolValue != "true"}
