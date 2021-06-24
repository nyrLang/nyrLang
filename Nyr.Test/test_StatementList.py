import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testMultipleStrings():
	parser = Parser()
	ast = parser.parse("'Hello'; '42';")

	body = ast.body
	assert len(body) == 2

	expression: Node.Node = body[0].expression
	assert expression.type == "StringLiteral"
	assert expression.value == "Hello"

	expression: Node.Node = body[1].expression
	assert expression.type == "StringLiteral"
	assert expression.value == "42"


def testMutlipleNumbers():
	parser = Parser()
	ast = parser.parse("1; 163543516;")

	body = ast.body
	assert len(body) == 2

	expression: Node.Node = body[0].expression
	assert expression.type == "NumericLiteral"
	assert expression.value == 1

	expression: Node.Node = body[1].expression
	assert expression.type == "NumericLiteral"
	assert expression.value == 163543516


def testMixed():
	parser = Parser()
	ast = parser.parse("'Hello'; 42;")

	body = ast.body
	assert len(body) == 2

	expression: Node.Node = body[0].expression
	assert expression.type == "StringLiteral"
	assert expression.value == "Hello"

	expression: Node.Node = body[1].expression
	assert expression.type == "NumericLiteral"
	assert expression.value == 42
