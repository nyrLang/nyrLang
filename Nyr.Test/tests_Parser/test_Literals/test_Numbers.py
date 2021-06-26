import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testInteger():
	parser = Parser()

	for test in ["42;", "   42;   ", "42  ;"]:
		ast = parser.parse(test)

		assert ast.type == "Program"
		body = ast.body

		assert len(body) == 1

		node = body[0]

		assert isinstance(node, Node.ExpressionStatement)

		assert node.type == "ExpressionStatement"

		expression = node.expression

		assert isinstance(expression, Node.Literal)
		assert expression.type == "IntegerLiteral"
		assert expression.value == 42


def testFloat():
	parser = Parser()

	for test in ["3.141;", "   3.141;   ", "3.141  ;"]:
		ast = parser.parse(test)

		assert ast.type == "Program"
		body = ast.body

		assert len(body) == 1

		node = body[0]

		assert isinstance(node, Node.ExpressionStatement)

		expression = node.expression

		assert isinstance(expression, Node.Literal)
		assert expression.type == "FloatLiteral"
		assert expression.value == 3.141
