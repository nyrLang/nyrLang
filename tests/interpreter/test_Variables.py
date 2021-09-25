import pytest

from nyr.interpreter.interpreter import Interpreter
from nyr.parser.parser import Parser


def testUninitializedVariable():
	ast = Parser().parse("let x;")
	env = Interpreter().interpret(ast)

	assert env == {'x': None}


@pytest.mark.parametrize(
	("code", "expected"), (
		("let x; let y;", {'x': None, 'y': None}),
		("let x, y;", {'x': None, 'y': None}),
	),
)
def testMultipleUninitializedVariables(code: str, expected):
	ast = Parser().parse(code)
	env = Interpreter().interpret(ast)

	assert env == expected


@pytest.mark.parametrize(
	("code", "expected"), (
		('let string = "I am a string!";', {"string": "I am a string!"}),
		("let int = 42;", {"int": 42}),
		("let float = 3.14159;", {"float": 3.14159}),
		("let bool = false;", {"bool": False}),
		("let none = null;", {"none": None}),
	),
)
def testTypeAssignments(code: str, expected):
	ast = Parser().parse(code)
	env = Interpreter().interpret(ast)

	assert env == expected


def testMixedInitialize():
	ast = Parser().parse("let x, y = 7, z;")
	env = Interpreter().interpret(ast)

	assert env == {
		'x': None,
		'y': 7,
		'z': None,
	}


def testAssignWithBinaryExpr():
	ast = Parser().parse("""
		let x = 4;
		let y = 7;
		let z = x + y;
	""")

	env = Interpreter().interpret(ast)

	assert env == {
		"x": 4,
		"y": 7,
		"z": 11,
	}


@pytest.mark.parametrize(
	("code"), (
		("let x; let x;"),
		("let x, x;"),
	),
)
def testVarExists(code: str):
	ast = Parser().parse(code)

	# FIXME: Wrong error returned from code
	with pytest.raises(Exception, match='Unknown variable "None"'):
		Interpreter().interpret(ast)


def testVarNotExists():
	ast = Parser().parse("x = 4;")

	with pytest.raises(Exception, match='Variable "x" does not exist in available scope'):
		Interpreter().interpret(ast)