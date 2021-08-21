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


def testDoWhile():
	ast = Parser().parse("""
		let x = 0;
		do {
			x += 7;
		} while (false);
	""")

	out = Interpreter().interpret(ast, Env())

	assert out == {"x": 7}
