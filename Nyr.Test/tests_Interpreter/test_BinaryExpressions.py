from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


def testAddition():
	ast = Parser().parse("let res = 1 + 2;")

	out = Interpreter().interpret(ast, Env())

	assert len(out) == 1

	assert out["res"] == 3


def testSubtraction():
	ast = Parser().parse("let res = 1 - 2;")

	out = Interpreter().interpret(ast, Env())

	assert len(out) == 1

	assert out["res"] == -1


def testMultiplication():
	ast = Parser().parse("let res = 3 * 4;")

	out = Interpreter().interpret(ast, Env())

	assert len(out) == 1

	assert out["res"] == 12


def testDivision():
	ast = Parser().parse("let res = 9 / 3;")

	out = Interpreter().interpret(ast, Env())

	assert len(out) == 1

	assert type(out["res"]) == int
	assert out["res"] == 3

	# -------------------------

	ast = Parser().parse("let res = 3 / 2;")
	out = Interpreter().interpret(ast, Env())

	assert len(out) == 1

	assert type(out["res"]) == float
	assert out["res"] == (3 / 2)


def testModulo():
	ast = Parser().parse("let res = 9 % 2;")

	out = Interpreter().interpret(ast, Env())

	assert len(out) == 1

	assert out["res"] == 1
