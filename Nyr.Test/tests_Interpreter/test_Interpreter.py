from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


def testEmptyStatement():
	ast = Parser().parse(";;")
	env = Interpreter().interpret(ast)

	assert env == dict()
