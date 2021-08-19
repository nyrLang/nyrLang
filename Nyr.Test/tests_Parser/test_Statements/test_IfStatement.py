import json

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testSimpleIfStatement():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				if (x) {
					x = 1;
				}
			"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "IfStatement",
				"test": {
					"type": "Identifier",
					"name": "x",
				},
				"consequent": {
					"type": "BlockStatement",
					"body": [
						{
							"type": "ExpressionStatement",
							"expression": {
								"type": "AssignmentExpression",
								"operator": "=",
								"left": {
									"type": "Identifier",
									"name": "x",
								},
								"right": {
									"type": "IntegerLiteral",
									"value": 1,
								},
							},
						},
					],
				},
				"alternative": None,
			},
		],
	}

	assert ast == expected


def testIfStatementWithoutBlock():
	ast = json.loads(
		json.dumps(
			Parser().parse("if (x) x = 1;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "IfStatement",
				"test": {
					"type": "Identifier",
					"name": "x",
				},
				"consequent": {
					"type": "ExpressionStatement",
					"expression": {
						"type": "AssignmentExpression",
						"operator": "=",
						"left": {
							"type": "Identifier",
							"name": "x",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 1,
						},
					},
				},
				"alternative": None,
			},
		],
	}

	assert ast == expected


def testNestedIfStatement():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				if (x)
					if (y) { }
					else { }
			"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "IfStatement",
				"test": {
					"type": "Identifier",
					"name": "x",
				},
				"consequent": {
					"type": "IfStatement",
					"test": {
						"type": "Identifier",
						"name": "y",
					},
					"consequent": {
						"type": "BlockStatement",
						"body": [],
					},
					"alternative": {
						"type": "BlockStatement",
						"body": [],
					},
				},
				"alternative": None,
			},
		],
	}

	assert ast == expected


def testIfElseStatement():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				if (x) {
					x = 1;
				} else {
					x = 2;
				}
			"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "IfStatement",
				"test": {
					"type": "Identifier",
					"name": "x",
				},
				"consequent": {
					"type": "BlockStatement",
					"body": [
						{
							"type": "ExpressionStatement",
							"expression": {
								"type": "AssignmentExpression",
								"operator": "=",
								"left": {
									"type": "Identifier",
									"name": "x",
								},
								"right": {
									"type": "IntegerLiteral",
									"value": 1,
								},
							},
						},
					],
				},
				"alternative": {
					"type": "BlockStatement",
					"body": [
						{
							"type": "ExpressionStatement",
							"expression": {
								"type": "AssignmentExpression",
								"operator": "=",
								"left": {
									"type": "Identifier",
									"name": "x",
								},
								"right": {
									"type": "IntegerLiteral",
									"value": 2,
								},
							},
						},
					],
				},
			},
		],
	}

	assert ast == expected
