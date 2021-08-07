import pytest

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testEmptyString():
	ast = Parser().parse(r'"";')

	assert ast.type == "Program"

	body = ast.body
	assert len(body) == 1

	node = body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.Literal)
	assert expression.type == "StringLiteral"
	assert expression.value == ""


def testSimpleString():
	parser = Parser()

	for test in [r'"Hello";', r'    "Hello";    ', r'"Hello"  ;']:
		ast = parser.parse(test)

		assert ast.type == "Program"

		body = ast.body
		assert len(body) == 1

		node = body[0]

		assert isinstance(node, Node.ExpressionStatement)

		expression = node.expression

		assert isinstance(expression, Node.Literal)
		assert expression.type == "StringLiteral"
		assert expression.value == "Hello"


def testComplexString():
	parser = Parser()

	for test in [r'"Hello, World";', r'   "Hello, World";   ', r'"Hello, World"   ;']:
		ast = parser.parse(test)

		assert ast.type == "Program"

		body = ast.body
		assert len(body) == 1

		node = body[0]

		assert isinstance(node, Node.ExpressionStatement)

		expression = node.expression

		assert isinstance(expression, Node.Literal)
		assert expression.type == "StringLiteral"
		assert expression.value == "Hello, World"


def testUnclosedString():
	with pytest.raises(Exception):
		Parser().parse(r'"Unclosed string ahead!')
