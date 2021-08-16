import json

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testBlockStatement():
	ast = json.loads(
		json.dumps(
			Parser().parse("""{
				42;

				"Hello";
			}"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "BlockStatement",
				"body": [
					{
						"type": "ExpressionStatement",
						"expression": {
							"type": "IntegerLiteral",
							"value": 42,
						},
					},
					{
						"type": "ExpressionStatement",
						"expression": {
							"type": "StringLiteral",
							"value": "Hello",
						},
					},
				],
			},
		],
	}

	assert ast == expected


def testNestedBlockStatement():
	ast = json.loads(
		json.dumps(
			Parser().parse("""{
				42;

				{
					"Hello";
				}
			}"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "BlockStatement",
				"body": [
					{
						"type": "ExpressionStatement",
						"expression": {
							"type": "IntegerLiteral",
							"value": 42,
						},
					},
					{
						"type": "BlockStatement",
						"body": [
							{
								"type": "ExpressionStatement",
								"expression": {
									"type": "StringLiteral",
									"value": "Hello",
								},
							},
						],
					},
				],
			},
		],
	}

	assert ast == expected
