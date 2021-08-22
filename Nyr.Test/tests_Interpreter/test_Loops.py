from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


def testWhileLoop():
	ast = Parser().parse("""
		let x = 0;
		while (x < 5) {
			x += 1;
		}
	""")

	out = Interpreter().interpret(ast, Env())

	assert out == {"x": 5}


def testWhileLoopBreak():
	ast = Parser().parse("""
		let x = 0;
		while (x < 5) {
			x += 1;
			if (x == 2) {
				break;
			}
		}
	""")

	out = Interpreter().interpret(ast, Env())

	assert out == {"x": 2}


def testDoWhile():
	ast = Parser().parse("""
		let x = 0;
		do {
			x += 7;
		} while (false);
	""")

	out = Interpreter().interpret(ast, Env())

	assert out == {"x": 7}


def testDoWhileBreak():
	ast = Parser().parse("""
		let x = 0;
		do {
			x += 1;
			if (x == 9) {
				break;
			}
		} while (true);
	""")

	out = Interpreter().interpret(ast, Env())

	assert out == {"x": 9}


def testForLoop():
	ast = Parser().parse("""
		let x = 0;
		for (let i = 0; i < 10; i += 2) {
			x += i;
		}

		let y = 0;
		let i = 7;
		for (i = 0; i < 10; i += 2) {
			y += i;
		}
	""")

	out = Interpreter().interpret(ast, Env())

	assert out == {"i": 10, "x": 20, "y": 20}


def testForLoopBreak():
	ast = Parser().parse("""
		let x = 0;
		for (let i = 0; i < 10; i += 2) {
			x += i;
			if (i == 6) {
				break;
			}
		}

		let y = 0;
		let i = 7;
		for (i = 0; i < 10; i += 2) {
			y += i;
		}
	""")

	out = Interpreter().interpret(ast, Env())

	assert out == {"i": 10, "x": 12, "y": 20}
