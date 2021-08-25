import pytest

from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


@pytest.mark.parametrize(
	("xVal", "expectedY"), (
		(-4, "x is 2 or less"),
		(0, "x is 2 or less"),
		(2, "x is 2 or less"),
		(3, "x is greater than 2"),
		(99999999999999999, "x is greater than 2"),
	),
)
def testIfElse(xVal: int, expectedY: str):
	code = """
		let x = __xval__;
		let y = "";
		if (x > 2) {
			y = "x is greater than 2";
		} else {
			y = "x is 2 or less";
		}
	""".replace("__xval__", str(xVal))
	ast = Parser().parse(code)

	out = Interpreter().interpret(ast, Env())

	assert out == {"x": xVal, "y": expectedY}


@pytest.mark.parametrize(
	("operator", "expected"), (
		("&&", (True, False, False, False)),
		("||", (True, True, True, False)),
	),
)
def testLogicalOperatorsI(operator: str, expected: tuple[bool]):
	assert len(expected) == 4, f"expected input must be of lenght 4, input was: {len(expected)}"
	ast = Parser().parse(f"""
		let a, b, c, d;
		a = true {operator} true;
		b = true {operator} false;
		c = false {operator} true;
		d = false {operator} false;
	""")

	out = Interpreter().interpret(ast, Env())

	assert out == {
		"a": expected[0],
		"b": expected[1],
		"c": expected[2],
		"d": expected[3],
	}


@pytest.mark.parametrize(
	("operator", "expected"), (
		(r"^", (False, True, True, False)),
		(r"|", (True, True, True, False)),
		(r"&", (True, False, False, False)),
	),
)
def testBitwiseOperatorsI(operator: str, expected: tuple[bool]):
	assert len(expected) == 4, f"expected input must be of lenght 4, input was: {len(expected)}"
	ast = Parser().parse(f"""
		let a, b, c, d;
		a = true {operator} true;
		b = true {operator} false;
		c = false {operator} true;
		d = false {operator} false;
	""")

	out = Interpreter().interpret(ast, Env())

	assert out == {
		"a": expected[0],
		"b": expected[1],
		"c": expected[2],
		"d": expected[3],
	}
