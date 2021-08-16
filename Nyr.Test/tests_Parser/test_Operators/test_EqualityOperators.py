import json

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testEquals():
	ast = json.loads(
		json.dumps(
			Parser().parse("x > 0 == true;"),
			cls=Node.ComplexEncoder,
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
			cls=Node.ComplexEncoder,
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
