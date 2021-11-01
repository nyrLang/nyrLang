import pytest

from nyr.interpreter.interpreter import Interpreter
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("expr", "expectedRes"), (
		pytest.param(
			"1 + 2",
			3,
			id="add int",
		),
		pytest.param(
			"1 + 2.14",
			float(3.14),
			id="add float",
		),
		pytest.param(
			"1 - 2",
			-1,
			id="sub int",
		),
		pytest.param(
			"2 - 5.54",
			-3.54,
			id="sub float",
		),
		pytest.param(
			"3 * 4",
			12,
			id="mult int",
		),
		pytest.param(
			"6 * 2.5",
			15,
			id="mul float",
		),
		pytest.param(
			"9 / 3",
			int(3),
			id="div int",
		),
		pytest.param(
			"3 / 2",
			float(3 / 2),
			id="div float",
		),
		pytest.param(
			"9 % 2",
			1,
			id="mod int",
		),
	),
)
def testSimpleExpression(expr: str, expectedRes):
	ast = Parser().parse(f"let res = {expr};")
	env = Interpreter().interpret(ast)

	assert env == {"res": expectedRes}


@pytest.mark.parametrize(
	("expr", "expectedRes"), (
		pytest.param(
			"(1 + 2) * 3",
			9,
			id="add before multiply",
		),
		pytest.param(
			"(5 + 13) / 6",
			int(3),
			id="add before divide",
		),
		pytest.param(
			"(10 / 4) * 2",
			int(5),
			id="divide before multiply",
		),
		pytest.param(
			"(42 / 2) + 17",
			int(38),
			id="divide before add",
		),
		pytest.param(
			"((2 + 1.14) * 2) / 2",
			pytest.approx(3.14),
			id="add before multiply before divide",
		),
	),
)
def testParenthesizedExpressions(expr: str, expectedRes):
	ast = Parser().parse(f"let res = {expr};")
	env = Interpreter().interpret(ast)

	assert env == {"res": expectedRes}


def testDivideBy0():
	ast = Parser().parse("1 / 0;")

	with pytest.raises(ZeroDivisionError, match="Cannot divide by 0"):
		Interpreter().interpret(ast)


@pytest.mark.parametrize(
	("string1", "string2", "expectedStr"), (
		pytest.param(
			"Ba", "nabra",
			"Banabra",
			id="string 1",
		),
		pytest.param(
			"Spag", "hetti",
			"Spaghetti",
			id="string 2",
		),
		pytest.param(
			"string", "",
			"string",
			id="add empty",
		),
		pytest.param(
			"", "concat",
			"concat",
			id="append to empty",
		),
		pytest.param(
			"42", "77",
			"4277",
			id="add string numbers",
		),
	),
)
def testStringConcatenation(string1: str, string2: str, expectedStr: str):
	ast = Parser().parse(f'let res = "{string1}" + "{string2}";')
	env = Interpreter().interpret(ast)

	assert env == {"res": expectedStr}
