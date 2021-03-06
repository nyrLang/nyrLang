import itertools
import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


def testWhileStatement():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				while (x > 10) {
					x -= 1;
				}
			"""),
			cls=node.ComplexEncoder,
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
			cls=node.ComplexEncoder,
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


testForStatementInit = {
	"type": "VariableStatement",
	"declarations": [{
		"type": "VariableDeclaration",
		"id": {"type": "Identifier", "name": "i"},
		"init": {"type": "IntegerLiteral", "value": 0},
	}],
}
testForStatementTest = {
	"type": "BinaryExpression",
	"operator": "<",
	"left": {"type": "Identifier", "name": "i"},
	"right": {"type": "IntegerLiteral", "value": 10},
}
testForStatementUpdate = {
	"type": "AssignmentExpression",
	"operator": "+=",
	"left": {"type": "Identifier", "name": "i"},
	"right": {"type": "IntegerLiteral", "value": 1},
}


@pytest.mark.parametrize(
	("init", "test", "update"),
	list(
		itertools.product(
			*zip(
				[testForStatementInit, testForStatementTest, testForStatementUpdate],
				itertools.repeat(None),
			),
		),
	),
)
def testForStatement(init, test, update):
	init_ = "" if init is None else "let i = 0"
	test_ = "" if test is None else "i < 10"
	update_ = "" if update is None else "i += 1"

	code = f"for ({init_}; {test_}; {update_}) " + "{ x += i; }"

	ast = json.loads(
		json.dumps(
			Parser().parse(code),
			cls=node.ComplexEncoder,
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
				"body": {
					"type": "BlockStatement",
					"body": [{
						"type": "ExpressionStatement",
						"expression": {
							"type": "AssignmentExpression",
							"operator": "+=",
							"left": {"type": "Identifier", "name": "x"},
							"right": {"type": "Identifier", "name": "i"},
						},
					}],
				},
			},
		],
	}

	assert ast == expected


def testForStatementPredefinedInit():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				let x = 0;
				let i = 7;
				for (i = 0; i < 10; i += 1) {
					x += i;
				}
			"""),
			cls=node.ComplexEncoder,
		),
	)

	assert ast == {
		"type": "Program",
		"body": [
			{
				"type": "VariableStatement",
				"declarations": [
					{
						"type": "VariableDeclaration",
						"id": {
							"type": "Identifier",
							"name": "x",
						},
						"init": {
							"type": "IntegerLiteral",
							"value": 0,
						},
					},
				],
			},
			{
				"type": "VariableStatement",
				"declarations": [
					{
						"type": "VariableDeclaration",
						"id": {
							"type": "Identifier",
							"name": "i",
						},
						"init": {
							"type": "IntegerLiteral",
							"value": 7,
						},
					},
				],
			},
			{
				"type": "ForStatement",
				"init": {
					"type": "AssignmentExpression",
					"operator": "=",
					"left": {
						"type": "Identifier",
						"name": "i",
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 0,
					},
				},
				"test": {
					"type": "BinaryExpression",
					"operator": "<",
					"left": {
						"type": "Identifier",
						"name": "i",
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 10,
					},
				},
				"update": {
					"type": "AssignmentExpression",
					"operator": "+=",
					"left": {
						"type": "Identifier",
						"name": "i",
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 1,
					},
				},
				"body": {
					"type": "BlockStatement",
					"body": [
						{
							"type": "ExpressionStatement",
							"expression": {
								"type": "AssignmentExpression",
								"operator": "+=",
								"left": {
									"type": "Identifier",
									"name": "x",
								},
								"right": {
									"type": "Identifier",
									"name": "i",
								},
							},
						},
					],
				},
			},
		],
	}
