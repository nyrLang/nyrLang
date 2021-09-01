import re

import pytest

from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Interpreter.Interpreter import MAXRECURSIONDEPTH
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

	env = Interpreter().interpret(ast)

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

	with pytest.raises(Exception, match=r'Incorrect amount of arguments given. Expected 2, got 1'):
		Interpreter().interpret(ast)


def testFunctionNotExists():
	ast = Parser().parse("""
		let x = 42;
		let y = 58;
		let z = 0;

		z = add(x, y);
	""")

	with pytest.raises(Exception, match=r'Function "add" does not exist in available scope'):
		Interpreter().interpret(ast)


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

		z = add(x, y);
	""")

	with pytest.raises(Exception, match=r'Function "add" already exists in available scope'):
		Interpreter().interpret(ast)


def testFunctionReturnValue():
	ast = Parser().parse("""
		def returnString() {
			let string = "Hello";

			string += ", World!";

			return string;
		}

		let s = returnString();
	""")

	env = Interpreter().interpret(ast)

	assert env == {"s": "Hello, World!"}


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

	env = Interpreter().interpret(ast)

	assert env == {
		"fac": 120,
	}


def testRecursionOverflow():
	ast = Parser().parse("""
		def recursiveFunction() {
			recursiveFunction();
		}

		recursiveFunction();
	""")

	with pytest.raises(Exception, match=re.escape(f'Exceeded recursion depth of {MAXRECURSIONDEPTH} in function "recursiveFunction"')):
		Interpreter().interpret(ast)
