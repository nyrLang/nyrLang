import pytest

from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


def testFunction():
	ast = Parser().parse("""
		let x = 42;
		let y = 58;
		let z = 0;

		def add(num1, num2) {
			return num1 + num2;
		}

		z = add(x, y);
	""")

	env = Interpreter().interpret(ast, Env())

	assert env == {
		"x": 42,
		"y": 58,
		"z": 100,
	}


def testFunctionWithIncorrectArguments():
	ast = Parser().parse("""
		let x = 42;
		let y = 58;
		let z = 0;

		def add(num1, num2) {
			return num1 + num2;
		}

		z = add(x);
	""")

	with pytest.raises(Exception, match='Incorrect amount of arguments given. Expected 2, got 1'):
		Interpreter().interpret(ast, Env())


def testFunctionNotExists():
	ast = Parser().parse("""
		let x = 42;
		let y = 58;
		let z = 0;

		z = add(x, y);
	""")

	with pytest.raises(Exception, match='Function "add" does not exist in available scope'):
		Interpreter().interpret(ast, Env())


def testFunctionAlreadyExists():
	ast = Parser().parse("""
		let x = 42;
		let y = 58;
		let z = 0;

		def add(num1, num2) {
			return num1 + num2;
		}

		def add(num1, num2) {
			return num1 + num2;
		}

		z = add(x);
	""")

	with pytest.raises(Exception, match='Function "add" already exists in available scope'):
		Interpreter().interpret(ast, Env())


@pytest.mark.xfail(reason="Recursion not yet working")
def testRecursion():
	ast = Parser().parse("""
		def factorial(x) {
			if (x <= 1) {
				return 1;
			} else {
				return x * factorial(x - 1);
			}
		}

		let fac = factorial(5);
	""")

	env = Interpreter().interpret(ast, Env())

	assert env == {
		"fac": 120,
	}
