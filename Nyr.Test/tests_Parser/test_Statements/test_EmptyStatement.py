import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testEmptyStatement():
	ast = Parser().parse(";")

	assert len(ast.body) == 1

	assert isinstance(ast.body[0], Node.EmptyStatement)
	assert ast.body[0].type == "EmptyStatement"
