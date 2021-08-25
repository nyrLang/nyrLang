import json

from Nyr.Parser import Node
from Nyr.Parser.Parser import Parser


def testMultipleStrings():
	ast = json.loads(
		json.dumps(
			Parser().parse('"Hello"; "42";'),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "StringLiteral",
					"value": "Hello",
				},
			},
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "StringLiteral",
					"value": "42",
				},
			},
		],
	}

	assert ast == expected


def testMutlipleNumbers():
	ast = json.loads(
		json.dumps(
			Parser().parse("1; 163543516;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "IntegerLiteral",
					"value": 1,
				},
			},
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "IntegerLiteral",
					"value": 163543516,
				},
			},
		],
	}

	assert ast == expected


def testMutlipleFloats():
	ast = json.loads(
		json.dumps(
			Parser().parse("3.141; 2.718;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "FloatLiteral",
					"value": 3.141,
				},
			},
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "FloatLiteral",
					"value": 2.718,
				},
			},
		],
	}

	assert ast == expected


def testMixed():
	ast = json.loads(
		json.dumps(
			Parser().parse('"Hello, World!"; 42; 3.141;'),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "StringLiteral",
					"value": "Hello, World!",
				},
			},
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
					"type": "FloatLiteral",
					"value": 3.141,
				},
			},
		],
	}

	assert ast == expected
