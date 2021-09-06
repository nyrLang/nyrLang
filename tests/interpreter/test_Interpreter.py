from nyr.interpreter.interpreter import Interpreter
from nyr.parser.parser import Parser


def testEmptyStatement():
	ast = Parser().parse(";;")
	env = Interpreter().interpret(ast)

	assert env == dict()


def testInterpretMultiple():
	parser = Parser()
	interpreter = Interpreter()

	for i in range(20):
		ast = parser.parse(f"let x = {i};")
		env = interpreter.interpret(ast)

		assert env == {"x": i}
