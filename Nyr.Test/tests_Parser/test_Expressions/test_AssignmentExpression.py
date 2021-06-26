import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testSimpleAssignment():
	ast = Parser().parse("x = 42;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.ComplexExpression)
	assert expression.operator == "="

	left = expression.left
	assert isinstance(left, Node.Identifier)
	assert left.name == "x"

	right = expression.right
	assert isinstance(right, Node.Literal)
	assert right.type == "IntegerLiteral"
	assert right.value == 42


def testChainedSimpleAssignment():
	ast = Parser().parse("x = y = 42;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression
	assert isinstance(expression, Node.ComplexExpression)
	assert expression.operator == "="

	left0 = expression.left
	assert isinstance(left0, Node.Identifier)
	assert left0.name == "x"

	right0 = expression.right
	assert isinstance(right0, Node.ComplexExpression)
	assert right0.operator == "="

	left1 = right0.left
	assert isinstance(left1, Node.Identifier)
	assert left1.name == "y"

	right1 = right0.right
	assert isinstance(right1, Node.Literal)
	assert right1.type == "IntegerLiteral"
	assert right1.value == 42


def testComplexAssignment():
	ast = Parser().parse("x += 3;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.ComplexExpression)
	assert expression.operator == "+="

	left = expression.left
	assert isinstance(left, Node.Identifier)
	assert left.name == "x"

	right = expression.right
	assert isinstance(right, Node.Literal)
	assert right.type == "IntegerLiteral"
	assert right.value == 3
