import pytest

from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


def testUninitializedVariable():
	ast = Parser().parse("let x;")
	out = Interpreter().interpret(ast, Env())

	assert out == {'x': None}


@pytest.mark.parametrize(
	("code", "expected"), (
		("let x; let y;", {'x': None, 'y': None}),
		("let x; let y;", {'x': None, 'y': None}),
	),
)
def testMultipleUninitializedVariables(code: str, expected):
	ast = Parser().parse(code)
	out = Interpreter().interpret(ast, Env())

	assert out == expected


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
	out = Interpreter().interpret(ast, Env())

	assert out == expected


def testMixedInitialize():
	ast = Parser().parse("let x, y = 7, z;")
	out = Interpreter().interpret(ast, Env())

	expected = {
		'x': None,
		'y': 7,
		'z': None,
	}

	assert out == expected


def testAssignWithBinaryExpr():
	ast = Parser().parse("""
		let x = 4;
		let y = 7;
		let z = x + y;
	""")

	env = Interpreter().interpret(ast, Env())

	expected = {
		"x": 4,
		"y": 7,
		"z": 11,
	}

	assert env == expected
