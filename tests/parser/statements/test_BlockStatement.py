import json

from nyr.parser import node
from nyr.parser.parser import Parser


def testBlockStatement():
	ast = json.loads(
		json.dumps(
			Parser().parse("""{
				42;

				"Hello";
			}"""),
			cls=node.ComplexEncoder,
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
			cls=node.ComplexEncoder,
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
