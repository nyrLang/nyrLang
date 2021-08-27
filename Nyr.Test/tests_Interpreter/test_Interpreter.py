from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


def testEmptyStatement():
	ast = Parser().parse(";;")
	env = Interpreter(ast).interpret()

	assert env == dict()
