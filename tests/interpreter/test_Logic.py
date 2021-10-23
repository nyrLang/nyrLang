import pytest

from nyr.interpreter.interpreter import Interpreter
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("xVal", "expectedY"), (
		pytest.param(-4, "x is 2 or less"),
		pytest.param(0, "x is 2 or less"),
		pytest.param(2, "x is 2 or less"),
		pytest.param(3, "x is greater than 2"),
		pytest.param(99999999999999999, "x is greater than 2"),
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
	env = Interpreter().interpret(ast)

	assert env == {"x": xVal, "y": expectedY}


@pytest.mark.parametrize(
	("operator", "expected"), (
		pytest.param("&&", (True, False, False, False), id="and"),
		pytest.param("||", (True, True, True, False), id="or"),
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

	env = Interpreter().interpret(ast)

	assert env == {
		"a": expected[0],
		"b": expected[1],
		"c": expected[2],
		"d": expected[3],
	}


@pytest.mark.parametrize(
	("operator", "expected"), (
		pytest.param(r"^", (False, True, True, False), id="bitwise xor"),
		pytest.param(r"|", (True, True, True, False), id="bitwise or"),
		pytest.param(r"&", (True, False, False, False), id="bitwise and"),
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

	env = Interpreter().interpret(ast)

	assert env == {
		"a": expected[0],
		"b": expected[1],
		"c": expected[2],
		"d": expected[3],
	}
