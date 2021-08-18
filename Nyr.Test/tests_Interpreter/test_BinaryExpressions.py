import pytest

from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser

deadInterpreter = pytest.mark.xfail(raises=NotImplementedError, reason="Interpreter is currently dead code", run=False)


@deadInterpreter
def testAddition():
	ast = Parser().parse("let res = 1 + 2;")

	out = Interpreter().interpret(ast, Env())

	assert len(out) == 1

	assert out["res"] == 3


@deadInterpreter
def testSubtraction():
	ast = Parser().parse("let res = 1 - 2;")

	out = Interpreter().interpret(ast, Env())

	assert len(out) == 1

	assert out["res"] == -1


@deadInterpreter
def testMultiplication():
	ast = Parser().parse("let res = 3 * 4;")

	out = Interpreter().interpret(ast, Env())

	assert len(out) == 1

	assert out["res"] == 12


@deadInterpreter
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
