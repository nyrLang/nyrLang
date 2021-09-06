import json
import re

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


def testSimpleAssignment():
	ast = json.loads(
		json.dumps(
			Parser().parse("x = 42;"),
			cls=node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
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
						"value": 42,
					},
				},
			},
		],
	}

	assert ast == expected


def testChainedSimpleAssignment():
	ast = json.loads(
		json.dumps(
			Parser().parse("x = y = 42;"),
			cls=node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
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
						"type": "AssignmentExpression",
						"operator": "=",
						"left": {
							"type": "Identifier",
							"name": "y",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 42,
						},
					},
				},
			},
		],
	}

	assert ast == expected


def testComplexAssignment():
	ast = json.loads(
		json.dumps(
			Parser().parse("x += 3;"),
			cls=node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
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
						"type": "IntegerLiteral",
						"value": 3,
					},
				},
			},
		],
	}

	assert ast == expected


def testInvalidAssignment():
	with pytest.raises(Exception, match=re.escape("Invalid left-hand side in assignment expression: nyr.parser.Node.Literal(IntegerLiteral, 1); expected: Identifier, MemberExpression")):
		Parser().parse("1 = 2;")
