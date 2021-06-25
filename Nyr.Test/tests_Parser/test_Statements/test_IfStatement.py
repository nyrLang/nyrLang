import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testSimpleIfStatement():
	ast = Parser().parse("""
		if (x) {
			x = 1;
		}
	""")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.IfStatement)
	assert isinstance(node.test, Node.Identifier)
	assert node.test.name == "x"

	assert isinstance(node.consequent, Node.BlockStatement)

	consequent = node.consequent.body[0]
	assert isinstance(consequent, Node.ExpressionStatement)

	expression = consequent.expression
	assert isinstance(expression, Node.AssignmentExpression)
	assert expression.operator == "="

	left = expression.left
	assert isinstance(left, Node.Identifier)
	assert left.name == "x"

	right = expression.right
	assert isinstance(right, Node.IntegerLiteral)
	assert right.value == 1

	assert node.alternative is None


def testIfStatementWithoutBlock():
	ast = Parser().parse("if (x) x = 1;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.IfStatement)
	assert isinstance(node.test, Node.Identifier)
	assert node.test.name == "x"

	assert isinstance(node.consequent, Node.ExpressionStatement)

	expression = node.consequent.expression

	assert isinstance(expression, Node.AssignmentExpression)
	assert expression.operator == "="

	left = expression.left
	assert isinstance(left, Node.Identifier)
	assert left.name == "x"

	right = expression.right
	assert isinstance(right, Node.IntegerLiteral)
	assert right.value == 1

	assert node.alternative is None


def testNestedIfStatement():
	ast = Parser().parse("""
	if (x)
		if (y) { }
		else { }
	""")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.IfStatement)
	assert node.alternative is None

	assert isinstance(node.test, Node.Identifier)
	assert node.test.name == "x"

	assert isinstance(node.consequent, Node.IfStatement)
	nested = node.consequent

	assert isinstance(nested.test, Node.Identifier)
	assert nested.test.name == "y"

	assert isinstance(nested.consequent, Node.BlockStatement)
	assert len(nested.consequent.body) == 0

	assert isinstance(nested.alternative, Node.BlockStatement)
	assert len(nested.alternative.body) == 0


def testIfElseStatement():
	ast = Parser().parse("""
		if (x) {
			x = 1;
		} else {
			x = 2;
		}
	""")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.IfStatement)
	assert isinstance(node.test, Node.Identifier)
	assert node.test.name == "x"

	assert isinstance(node.consequent, Node.BlockStatement)

	consequent = node.consequent.body[0]
	assert isinstance(consequent, Node.ExpressionStatement)

	expression0 = consequent.expression
	assert isinstance(expression0, Node.AssignmentExpression)
	assert expression0.operator == "="

	left0 = expression0.left
	assert isinstance(left0, Node.Identifier)
	assert left0.name == "x"

	right0 = expression0.right
	assert isinstance(right0, Node.IntegerLiteral)
	assert right0.value == 1

	assert isinstance(node.alternative, Node.BlockStatement)

	alternative = node.alternative.body[0]
	assert isinstance(alternative, Node.ExpressionStatement)

	expression1 = alternative.expression
	assert isinstance(expression1, Node.AssignmentExpression)
	assert expression1.operator == "="

	left1 = expression1.left
	assert isinstance(left1, Node.Identifier)
	assert left1.name == "x"

	right1 = expression1.right
	assert isinstance(right1, Node.IntegerLiteral)
	assert right1.value == 2
