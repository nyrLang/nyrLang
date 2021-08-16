import json

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testAnd():
	ast = json.loads(
		json.dumps(
			Parser().parse("x >= 5 && y <= 20;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "LogicalExpression",
					"operator": "&&",
					"left": {
						"type": "BinaryExpression",
						"operator": ">=",
						"left": {
							"type": "Identifier",
							"name": "x",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 5,
						},
					},
					"right": {
						"type": "BinaryExpression",
						"operator": "<=",
						"left": {
							"type": "Identifier",
							"name": "y",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 20,
						},
					},
				},
			},
		],
	}

	assert ast == expected


def testOr():
	ast = json.loads(
		json.dumps(
			Parser().parse("x > 5 || y < 20;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "LogicalExpression",
					"operator": "||",
					"left": {
						"type": "BinaryExpression",
						"operator": ">",
						"left": {
							"type": "Identifier",
							"name": "x",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 5,
						},
					},
					"right": {
						"type": "BinaryExpression",
						"operator": "<",
						"left": {
							"type": "Identifier",
							"name": "y",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 20,
						},
					},
				},
			},
		],
	}

	assert ast == expected
