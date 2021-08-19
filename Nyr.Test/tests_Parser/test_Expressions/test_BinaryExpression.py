import json

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testBinaryExpressionAdd():
	ast = json.loads(
		json.dumps(
			Parser().parse("1 + 2;"),
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
					"operator": "+",
					"left": {
						"type": "IntegerLiteral",
						"value": 1,
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 2,
					},
				},
			},
		],
	}

	assert ast == expected


def testBinaryExpressionNested():
	ast = json.loads(
		json.dumps(
			Parser().parse("3 + 2 - 2;"),
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
					"operator": "-",
					"left": {
						"type": "BinaryExpression",
						"operator": "+",
						"left": {
							"type": "IntegerLiteral",
							"value": 3,
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 2,
						},
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 2,
					},
				},
			},
		],
	}

	assert ast == expected


def testBinaryExpressionMixed():
	ast = json.loads(
		json.dumps(
			Parser().parse("1 + 2 * 3;"),
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
					"operator": "+",
					"left": {
						"type": "IntegerLiteral",
						"value": 1,
					},
					"right": {
						"type": "BinaryExpression",
						"operator": "*",
						"left": {
							"type": "IntegerLiteral",
							"value": 2,
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 3,
						},
					},
				},
			},
		],
	}

	assert ast == expected


def testBinaryExpressionMultiply():
	ast = json.loads(
		json.dumps(
			Parser().parse("2 * 3;"),
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
					"operator": "*",
					"left": {
						"type": "IntegerLiteral",
						"value": 2,
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 3,
					},
				},
			},
		],
	}

	assert ast == expected


def testBinaryExpressionNestedMultiply():
	ast = json.loads(
		json.dumps(
			Parser().parse("1 * 2 * 3;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [{
			"type": "ExpressionStatement",
			"expression": {
				"type": "BinaryExpression",
				"operator": "*",
				"left": {
					"type": "BinaryExpression",
					"operator": "*",
					"left": {"type": "IntegerLiteral", "value": 1},
					"right": {"type": "IntegerLiteral", "value": 2},
				},
				"right": {"type": "IntegerLiteral", "value": 3},
			},
		}],
	}

	assert ast == expected


def testBinaryExpressionParenthesisPriority():
	ast = json.loads(
		json.dumps(
			Parser().parse("(1 + 2) * 3;"),
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
					"operator": "*",
					"left": {
						"type": "BinaryExpression",
						"operator": "+",
						"left": {
							"type": "IntegerLiteral",
							"value": 1,
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 2,
						},
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 3,
					},
				},
			},
		],
	}

	assert ast == expected
