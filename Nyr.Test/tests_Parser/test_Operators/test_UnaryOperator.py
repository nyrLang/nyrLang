import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testMinusOperator():
	ast = Parser().parse("-x;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.UnaryExpression)
	assert expression.operator == "-"

	assert isinstance(expression.argument, Node.Identifier)
	assert expression.argument.name == "x"


def testNotOperator():
	ast = Parser().parse("!x;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.UnaryExpression)
	assert expression.operator == "!"

	assert isinstance(expression.argument, Node.Identifier)
	assert expression.argument.name == "x"
