import json

from nyr.parser import node
from nyr.parser.parser import Parser


def testEquals():
	ast = json.loads(
		json.dumps(
			Parser().parse("x > 0 == true;"),
			cls=node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "BinaryExpression",
					"operator": "==",
					"left": {
						"type": "BinaryExpression",
						"operator": ">",
						"left": {
							"type": "Identifier",
							"name": "x",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 0,
						},
					},
					"right": {
						"type": "BooleanLiteral",
						"value": True,
					},
				},
			},
		],
	}

	assert ast == expected


def testInequals():
	ast = json.loads(
		json.dumps(
			Parser().parse("x >= 0 != false;"),
			cls=node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "BinaryExpression",
					"operator": "!=",
					"left": {
						"type": "BinaryExpression",
						"operator": ">=",
						"left": {
							"type": "Identifier",
							"name": "x",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 0,
						},
					},
					"right": {
						"type": "BooleanLiteral",
						"value": False,
					},
				},
			},
		],
	}

	assert ast == expected
