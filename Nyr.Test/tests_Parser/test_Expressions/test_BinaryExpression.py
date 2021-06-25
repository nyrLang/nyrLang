import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testBinaryExpressionAdd():
	ast = Parser().parse("1 + 2;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.BinaryExpression)

	assert expression.operator == "+"

	left = expression.left
	assert isinstance(left, Node.IntegerLiteral)
	assert left.value == 1

	right = expression.right
	assert isinstance(right, Node.IntegerLiteral)
	assert right.value == 2


def testBinaryExpressionNested():
	ast = Parser().parse("3 + 2 - 2;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression
	assert isinstance(expression, Node.BinaryExpression)

	assert expression.operator == "-"

	left0 = expression.left
	assert isinstance(left0, Node.BinaryExpression)
	assert left0.operator == "+"

	left1 = left0.left
	assert isinstance(left1, Node.IntegerLiteral)
	assert left1.value == 3

	right1 = left0.right
	assert isinstance(right1, Node.IntegerLiteral)
	assert right1.value == 2

	right0 = expression.right
	assert isinstance(right0, Node.IntegerLiteral)
	assert right0.value == 2


def testBinaryExpressionMixed():
	ast = Parser().parse("1 + 2 * 3;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression
	assert isinstance(expression, Node.BinaryExpression)

	assert expression.operator == "+"

	left0 = expression.left
	assert isinstance(left0, Node.IntegerLiteral)
	assert left0.value == 1

	right0 = expression.right
	assert isinstance(right0, Node.BinaryExpression)
	assert right0.operator == "*"

	left1 = right0.left
	assert isinstance(left1, Node.IntegerLiteral)
	assert left1.value == 2

	right1 = right0.right
	assert isinstance(right1, Node.IntegerLiteral)
	assert right1.value == 3


def testBinaryExpressionMultiply():
	ast = Parser().parse("2 * 3;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.BinaryExpression)
	assert expression.operator == "*"

	left = expression.left
	assert isinstance(left, Node.IntegerLiteral)
	assert left.value == 2

	right = expression.right
	assert isinstance(right, Node.IntegerLiteral)
	assert right.value == 3


def testBinaryExpressionNestedMultiply():
	ast = Parser().parse("1 * 2 * 3;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression
	assert isinstance(expression, Node.BinaryExpression)

	assert expression.operator == "*"

	left0 = expression.left
	assert isinstance(left0, Node.BinaryExpression)
	assert left0.operator == "*"

	left1 = left0.left
	assert isinstance(left1, Node.IntegerLiteral)
	assert left1.value == 1

	right1 = left0.right
	assert isinstance(right1, Node.IntegerLiteral)
	assert right1.value == 2

	right0 = expression.right
	assert isinstance(right0, Node.IntegerLiteral)
	assert right0.value == 3


def testBinaryExpressionParenthesisPriority():
	ast = Parser().parse("(1 + 2) * 3;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression
	assert isinstance(expression, Node.BinaryExpression)

	assert expression.operator == "*"

	left0 = expression.left
	assert isinstance(left0, Node.BinaryExpression)
	assert left0.operator == "+"

	left1 = left0.left
	assert isinstance(left1, Node.IntegerLiteral)
	assert left1.value == 1

	right1 = left0.right
	assert isinstance(right1, Node.IntegerLiteral)
	assert right1.value == 2

	right0 = expression.right
	assert isinstance(right0, Node.IntegerLiteral)
	assert right0.value == 3