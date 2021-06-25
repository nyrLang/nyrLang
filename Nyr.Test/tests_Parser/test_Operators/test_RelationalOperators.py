import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testAll():
	operators = (">", ">=", "<", "<=")
	parser = Parser()

	for operator in operators:
		ast = parser.parse(f"x {operator} 0;")

		assert len(ast.body) == 1

		node = ast.body[0]
		assert isinstance(node, Node.ExpressionStatement)

		expression = node.expression
		assert isinstance(expression, Node.BinaryExpression)
		assert expression.operator == operator

		left = expression.left
		assert isinstance(left, Node.Identifier)
		assert left.name == "x"

		right = expression.right
		assert isinstance(right, Node.IntegerLiteral)
		assert right.value == 0
