import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testSimplePropertyAccess():
	ast = Parser().parse("x.y;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.MemberExpression)
	assert expression.computed is False

	assert isinstance(expression.object, Node.Identifier)
	assert expression.object.name == "x"

	assert isinstance(expression.property, Node.Identifier)
	assert expression.property.name == "y"


def testPropertyAssign():
	ast = Parser().parse("x.y = 1;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.ComplexExpression)
	assert expression.type == "AssignmentExpression"
	assert expression.operator == "="

	left = expression.left
	right = expression.right

	assert isinstance(left, Node.MemberExpression)
	assert left.computed is False

	assert isinstance(left.object, Node.Identifier)
	assert left.object.name == "x"

	assert isinstance(left.property, Node.Identifier)
	assert left.property.name == "y"

	assert isinstance(right, Node.Literal)
	assert right.type == "IntegerLiteral"
	assert right.value == 1


def testComputedPropertyAccess():
	ast = Parser().parse("x[0] = 1;")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.ComplexExpression)
	assert expression.type == "AssignmentExpression"
	assert expression.operator == "="

	left = expression.left
	right = expression.right

	assert isinstance(left, Node.MemberExpression)
	assert left.computed is True

	assert isinstance(left.object, Node.Identifier)
	assert left.object.name == "x"

	assert isinstance(left.property, Node.Literal)
	assert left.property.type == "IntegerLiteral"
	assert left.property.value == 0

	assert isinstance(right, Node.Literal)
	assert right.type == "IntegerLiteral"
	assert right.value == 1


def testChainedAndMixedPropertyAccess():
	""" AST as json:
	{
		type: "Program"
		body: [
			{
				type: "ExpressionStatement"
				expression: {
					type: "MemberExpression"
					computed: true
					object: {
						type: "MemberExpression"
						computed: false
						object: {
							type: "MemberExpression"
							computed: false
							object: {
								type: "Identifier"
								name: "a"
							}
							property: {
								type: "Identifier"
								name: "b"
							}
						}
						property: {
							type: "Identifier"
							name: "c"
					}
					property: {
						type: "StringLiteral"
						name: "d"
					}
				}
			}
		]
	}
	"""
	ast = Parser().parse("a.b.c['d'];")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression_c = node.expression
	assert isinstance(expression_c, Node.MemberExpression)
	assert expression_c.computed is True

	expression_b = expression_c.object
	assert isinstance(expression_b, Node.MemberExpression)
	assert expression_b.computed is False

	expression_a = expression_b.object
	assert isinstance(expression_a, Node.MemberExpression)
	assert expression_a.computed is False

	assert isinstance(expression_a.object, Node.Identifier)
	assert expression_a.object.name == "a"

	assert isinstance(expression_a.property, Node.Identifier)
	assert expression_a.property.name == "b"

	assert isinstance(expression_b.property, Node.Identifier)
	assert expression_b.property.name == "c"

	assert isinstance(expression_c.property, Node.Literal)
	assert expression_c.property.type == "StringLiteral"
	assert expression_c.property.value == "d"
