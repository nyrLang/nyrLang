import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testAnd():
	ast = Parser().parse("x >= 5 && y <= 20;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression
	assert isinstance(expression, Node.LogicalExpression)

	assert expression.operator == "&&"

	left = expression.left
	assert isinstance(left, Node.BinaryExpression)
	assert left.operator == ">="
	assert isinstance(left.left, Node.Identifier)
	assert left.left.name == "x"
	assert isinstance(left.right, Node.IntegerLiteral)
	assert left.right.value == 5

	right = expression.right
	assert isinstance(right, Node.BinaryExpression)
	assert right.operator == "<="
	assert isinstance(right.left, Node.Identifier)
	assert right.left.name == "y"
	assert isinstance(right.right, Node.IntegerLiteral)
	assert right.right.value == 20


def testOr():
	ast = Parser().parse("x > 5 || y < 20;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression
	assert isinstance(expression, Node.LogicalExpression)

	assert expression.operator == "||"

	left = expression.left
	assert isinstance(left, Node.BinaryExpression)
	assert left.operator == ">"
	assert isinstance(left.left, Node.Identifier)
	assert left.left.name == "x"
	assert isinstance(left.right, Node.IntegerLiteral)
	assert left.right.value == 5

	right = expression.right
	assert isinstance(right, Node.BinaryExpression)
	assert right.operator == "<"
	assert isinstance(right.left, Node.Identifier)
	assert right.left.name == "y"
	assert isinstance(right.right, Node.IntegerLiteral)
	assert right.right.value == 20
