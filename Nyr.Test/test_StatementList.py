from Nyr.Node import Node
from Nyr.Parser import Parser

"""
{
	"type": "Program",
	"body": [
		{
			"type": "ExpressionStatement",
			"expression": {
				"type": "StringLiteral",
				"value": "Hello"
				}
			},
			{
			"type": "ExpressionStatement",
			"expression": {
				"type": "NumericLiteral",
				"value": 42
			}
		}
	]
}
"""


def testMultipleStrings():
	parser = Parser()
	ast = parser.parse("'Hello'; '42';")

	body = ast.get("body")
	assert len(body) == 2

	expression = body[0].get("expression")
	assert expression.get("type") == Node.StringLiteral
	assert expression.get("value") == "Hello"

	expression = body[1].get("expression")
	assert expression.get("type") == Node.StringLiteral
	assert expression.get("value") == "42"


def testMutlipleNumbers():
	parser = Parser()
	ast = parser.parse("1; 163543516;")

	body = ast.get("body")
	assert len(body) == 2

	expression = body[0].get("expression")
	assert expression.get("type") == Node.NumericLiteral
	assert expression.get("value") == 1

	expression = body[1].get("expression")
	assert expression.get("type") == Node.NumericLiteral
	assert expression.get("value") == 163543516


def testMixed():
	parser = Parser()
	ast = parser.parse("'Hello'; 42;")

	body = ast.get("body")
	assert len(body) == 2

	expression = body[0].get("expression")
	assert expression.get("type") == Node.StringLiteral
	assert expression.get("value") == "Hello"

	expression = body[1].get("expression")
	assert expression.get("type") == Node.NumericLiteral
	assert expression.get("value") == 42
