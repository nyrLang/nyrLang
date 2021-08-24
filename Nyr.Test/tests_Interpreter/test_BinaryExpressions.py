import pytest

from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


@pytest.mark.parametrize(
	("expr", "expectedRes"), (
		("1 + 2", 3),
		("1 - 2", -1),
		("3 * 4", 12),
		("9 / 3", int(3)),
		("3 / 2", float(3 / 2)),
		("9 % 2", 1),
	),
)
def testSimpleExpression(expr: str, expectedRes):
	ast = Parser().parse(f"let res = {expr};")
	env = Interpreter().interpret(ast, Env())

	assert env == {"res": expectedRes}


def testDivideBy0():
	ast = Parser().parse("1 / 0;")

	with pytest.raises(ZeroDivisionError, match="Cannot divide by 0"):
		Interpreter().interpret(ast, Env())


@pytest.mark.parametrize(
	("string1", "string2", "expectedStr"), (
		("Ba", "nabra", "Banabra"),
		("Spag", "hetti", "Spaghetti"),
		("string", "", "string"),
		("", "concat", "concat"),
		("42", "77", "4277"),
	),
)
def testStringConcatenation(string1: str, string2: str, expectedStr: str):
	ast = Parser().parse(f'let res = "{string1}" + "{string2}";')
	env = Interpreter().interpret(ast, Env())

	assert env == {"res": expectedStr}
