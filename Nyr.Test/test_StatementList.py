import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testMultipleStrings():
	parser = Parser()
	ast = parser.parse("'Hello'; '42';")

	body = ast.body
	assert len(body) == 2

	# Check 'Hello'
	node = body[0]

	assert isinstance(node, Node.ExpressionStatement), f"{node.type} should be of type {Node.ExpressionStatement.type}"

	expression = node.expression

	assert isinstance(expression, Node.StringLiteral)
	assert expression.value == "Hello"

	# Check '42'
	node = body[1]
	assert isinstance(node, Node.ExpressionStatement), f"{node.type} should be of type {Node.ExpressionStatement.type}"

	expression = node.expression

	assert isinstance(expression, Node.StringLiteral)
	assert expression.value == "42"


def testMutlipleNumbers():
	parser = Parser()
	ast = parser.parse("1; 163543516;")

	body = ast.body
	assert len(body) == 2

	# Check 1
	node = body[0]

	assert isinstance(node, Node.ExpressionStatement), f"{node.type} should be of type {Node.ExpressionStatement.type}"

	expression = node.expression

	assert isinstance(expression, Node.IntegerLiteral)
	assert expression.value == 1

	# Check 163543516
	node = body[1]

	assert isinstance(node, Node.ExpressionStatement), f"{node.type} should be of type {Node.ExpressionStatement.type}"

	expression = node.expression

	assert isinstance(expression, Node.IntegerLiteral)
	assert expression.value == 163543516


def testMutlipleFloats():
	parser = Parser()
	ast = parser.parse("3.141; 2.718;")

	body = ast.body
	assert len(body) == 2

	# Check 3.141
	node = body[0]

	assert isinstance(node, Node.ExpressionStatement), f"{node.type} should be of type {Node.ExpressionStatement.type}"

	expression = node.expression

	assert isinstance(expression, Node.FloatLiteral)
	assert expression.value == 3.141

	# Check 2.718
	node = body[1]

	assert isinstance(node, Node.ExpressionStatement), f"{node.type} should be of type {Node.ExpressionStatement.type}"

	expression = node.expression

	assert isinstance(expression, Node.FloatLiteral)
	assert expression.value == 2.718


def testMixed():
	parser = Parser()
	ast = parser.parse("'Hello'; 42; 3.141;")

	body = ast.body
	assert len(body) == 3

	# Check 'Hello'
	node = body[0]

	assert isinstance(node, Node.ExpressionStatement), f"{node.type} should be of type {Node.ExpressionStatement.type}"

	expression = node.expression
	assert isinstance(expression, Node.StringLiteral)
	assert expression.value == "Hello"

	# Check 42
	node = body[1]

	assert isinstance(node, Node.ExpressionStatement), f"{node.type} should be of type {Node.ExpressionStatement.type}"

	expression = node.expression
	assert isinstance(expression, Node.IntegerLiteral)
	assert expression.value == 42

	# Check 3.141
	node = body[2]

	assert isinstance(node, Node.ExpressionStatement), f"{node.type} should be of type {Node.ExpressionStatement.type}"

	expression = node.expression
	assert isinstance(expression, Node.FloatLiteral)
	assert expression.value == 3.141
