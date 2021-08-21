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

	out = Interpreter().interpret(ast, Env())

	assert out == {
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

	with pytest.raises(Exception, match='Function with name "add" does not exist in available scope'):
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

	with pytest.raises(Exception, match='Function "add" already defined'):
		Interpreter().interpret(ast, Env())
