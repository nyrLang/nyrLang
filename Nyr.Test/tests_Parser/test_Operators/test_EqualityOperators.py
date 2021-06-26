import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testEquals():
	ast = Parser().parse("x > 0 == true;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression
	assert isinstance(expression, Node.ComplexExpression)
	assert expression.operator == "=="

	left0 = expression.left
	assert isinstance(left0, Node.ComplexExpression)
	assert left0.operator == ">"

	right0 = expression.right
	assert isinstance(right0, Node.Literal)
	assert right0.type == "BooleanLiteral"
	assert right0.value is True

	left1 = left0.left
	assert isinstance(left1, Node.Identifier)
	assert left1.name == "x"

	right1 = left0.right
	assert isinstance(right1, Node.Literal)
	assert right1.type == "IntegerLiteral"
	assert right1.value == 0


def testInEquals():
	ast = Parser().parse("x >= 0 != false;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression
	assert isinstance(expression, Node.ComplexExpression)
	assert expression.operator == "!="

	left0 = expression.left
	assert isinstance(left0, Node.ComplexExpression)
	assert left0.operator == ">="

	right0 = expression.right
	assert isinstance(right0, Node.Literal)
	assert right0.type == "BooleanLiteral"
	assert right0.value is False

	left1 = left0.left
	assert isinstance(left1, Node.Identifier)
	assert left1.name == "x"

	right1 = left0.right
	assert isinstance(right1, Node.Literal)
	assert right1.type == "IntegerLiteral"
	assert right1.value == 0
