import json

import pytest

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testWhileStatement():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				while (x > 10) {
					x -= 1;
				}
			"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "WhileStatement",
				"test": {
					"type": "BinaryExpression",
					"operator": ">",
					"left": {
						"type": "Identifier",
						"name": "x",
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 10,
					},
				},
				"body": {
					"type": "BlockStatement",
					"body": [
						{
							"type": "ExpressionStatement",
							"expression": {
								"type": "AssignmentExpression",
								"operator": "-=",
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
			},
		],
	}

	assert ast == expected


def testDoWhileStatement():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				do {
					x -= 1;
				} while (x > 10);
			"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "DoWhileStatement",
				"body": {
					"type": "BlockStatement",
					"body": [
						{
							"type": "ExpressionStatement",
							"expression": {
								"type": "AssignmentExpression",
								"operator": "-=",
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
				"test": {
					"type": "BinaryExpression",
					"operator": ">",
					"left": {
						"type": "Identifier",
						"name": "x",
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 10,
					},
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.parametrize(
	("code", "init", "test", "update", "body"), [
		( # full
			"for (let i = 0; i < 10; i += 1) { x += i; }", # code
			{ # init
				"type": "VariableStatement",
				"declarations": [{
					"type": "VariableDeclaration",
					"id": { "type": "Identifier", "name": "i"},
					"init": { "type": "IntegerLiteral", "value": 0},
				}],
			}, # /init
			{ # test
				"type": "BinaryExpression",
				"operator": "<",
				"left": { "type": "Identifier", "name": "i"},
				"right": { "type": "IntegerLiteral", "value": 10},
			}, # /test
			{ # update
				"type": "AssignmentExpression",
				"operator": "+=",
				"left": { "type": "Identifier", "name": "i"},
				"right": { "type": "IntegerLiteral", "value": 1},
			}, # /update
			{ # body
				"type": "BlockStatement",
				"body": [{
					"type": "ExpressionStatement",
					"expression": {
						"type": "AssignmentExpression",
						"operator": "+=",
						"left": { "type": "Identifier", "name": "x"},
						"right": { "type": "Identifier", "name": "i"},
					},
				}],
			}, # /body
		), # full
		( # missing init
			"for ( ; i < 10; i += 1) { x += i; }", # code
			None, # init
			{ # test
				"type": "BinaryExpression",
				"operator": "<",
				"left": { "type": "Identifier", "name": "i"},
				"right": { "type": "IntegerLiteral", "value": 10},
			}, # /test
			{ # update
				"type": "AssignmentExpression",
				"operator": "+=",
				"left": { "type": "Identifier", "name": "i"},
				"right": { "type": "IntegerLiteral", "value": 1},
			}, # /update
			{ # body
				"type": "BlockStatement",
				"body": [{
					"type": "ExpressionStatement",
					"expression": {
						"type": "AssignmentExpression",
						"operator": "+=",
						"left": { "type": "Identifier", "name": "x"},
						"right": { "type": "Identifier", "name": "i"},
					},
				}],
			}, # /body
		), # /missing init
		( # missing test
			"for (let i = 0 ; ; i += 1) { x += i; }", # code
			{ # init
				"type": "VariableStatement",
				"declarations": [{
					"type": "VariableDeclaration",
					"id": { "type": "Identifier", "name": "i"},
					"init": { "type": "IntegerLiteral", "value": 0},
				}],
			}, # /init, # init
			None, # /test
			{ # update
				"type": "AssignmentExpression",
				"operator": "+=",
				"left": { "type": "Identifier", "name": "i"},
				"right": { "type": "IntegerLiteral", "value": 1},
			}, # /update
			{ # body
				"type": "BlockStatement",
				"body": [{
					"type": "ExpressionStatement",
					"expression": {
						"type": "AssignmentExpression",
						"operator": "+=",
						"left": { "type": "Identifier", "name": "x"},
						"right": { "type": "Identifier", "name": "i"},
					},
				}],
			}, # /body
		), # /missing test
		( # missing update
			"for (let i = 0 ; i < 10; ) { x += i; }", # code
			{ # init
				"type": "VariableStatement",
				"declarations": [{
					"type": "VariableDeclaration",
					"id": { "type": "Identifier", "name": "i"},
					"init": { "type": "IntegerLiteral", "value": 0},
				}],
			}, # /init
			{ # test
				"type": "BinaryExpression",
				"operator": "<",
				"left": { "type": "Identifier", "name": "i"},
				"right": { "type": "IntegerLiteral", "value": 10},
			}, # /test
			None, # update
			{ # body
				"type": "BlockStatement",
				"body": [{
					"type": "ExpressionStatement",
					"expression": {
						"type": "AssignmentExpression",
						"operator": "+=",
						"left": { "type": "Identifier", "name": "x"},
						"right": { "type": "Identifier", "name": "i"},
					},
				}],
			}, # /body
		), # /missing update
		( # missing all
			"for ( ; ; ) { x += i; }", # code
			None, # init
			None, # test
			None, # update
			{ # body
				"type": "BlockStatement",
				"body": [{
					"type": "ExpressionStatement",
					"expression": {
						"type": "AssignmentExpression",
						"operator": "+=",
						"left": { "type": "Identifier", "name": "x"},
						"right": { "type": "Identifier", "name": "i"},
					},
				}],
			}, # /body
		), # /missing all
	],
)
def testForStatement(code: str, init, test, update, body):
	ast = json.loads(
		json.dumps(
			Parser().parse(code),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ForStatement",
				"init": init,
				"test": test,
				"update": update,
				"body": body,
			},
		],
	}

	print(f"\n\n{ast=}\n\n")
	print(f"\n\n{expected=}\n\n")

	assert ast == expected
