import re

import pytest

from nyr.interpreter.interpreter import Interpreter
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("operator"), (
		pytest.param("-", id="negative"),
		pytest.param("+", id="positive"),
		pytest.param("!", id="not"),
	),
)
def testUnaryNone(operator: str):
	ast = Parser().parse(f"let x = {operator}null;")

	with pytest.raises(Exception, match=re.escape(f'Cannot use {operator} on "null"')):
		Interpreter().interpret(ast)


@pytest.mark.parametrize(
	("operator"), (
		pytest.param("-", id="negative"),
		pytest.param("+", id="positive"),
	),
)
def testUnaryInteger(operator: str):
	ast = Parser().parse(f"let x = {operator}5;")
	env = Interpreter().interpret(ast)

	assert env == {
		"+": {"x": 5},
		"-": {"x": -5},
	}[operator]


@pytest.mark.parametrize(
	("boolValue"), (
		pytest.param("true", id="true -> false"),
		pytest.param("false", id="false -> true"),
	),
)
def testUnaryNotBool(boolValue: str):
	ast = Parser().parse(f"let x = !{boolValue};")
	env = Interpreter().interpret(ast)

	assert env == {"x": boolValue != "true"}
