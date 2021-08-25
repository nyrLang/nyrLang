import json

from Nyr.Parser import Node
from Nyr.Parser.Parser import Parser


def testDeclarationWithAssign():
	ast = json.loads(
		json.dumps(
			Parser().parse("let x = 42;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
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
							"value": 42,
						},
					},
				],
			},
		],
	}

	assert ast == expected


def testDeclarationWithoutAssign():
	ast = json.loads(
		json.dumps(
			Parser().parse("let x;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
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
						"init": None,
					},
				],
			},
		],
	}

	assert ast == expected


def testMultipleDeclarationsWithoutAssign():
	ast = json.loads(
		json.dumps(
			Parser().parse("let x, y;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
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
						"init": None,
					},
					{
						"type": "VariableDeclaration",
						"id": {
							"type": "Identifier",
							"name": "y",
						},
						"init": None,
					},
				],
			},
		],
	}

	assert ast == expected


def testMultipleDeclarationsWithPartialAssign():
	ast = json.loads(
		json.dumps(
			Parser().parse("let x, y = 42;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
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
						"init": None,
					},
					{
						"type": "VariableDeclaration",
						"id": {
							"type": "Identifier",
							"name": "y",
						},
						"init": {
							"type": "IntegerLiteral",
							"value": 42,
						},
					},
				],
			},
		],
	}

	assert ast == expected


def testMultipleDeclarationsWithAllAssign():
	ast = json.loads(
		json.dumps(
			Parser().parse("let x = 7, y = 42;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
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
							"value": 7,
						},
					},
					{
						"type": "VariableDeclaration",
						"id": {
							"type": "Identifier",
							"name": "y",
						},
						"init": {
							"type": "IntegerLiteral",
							"value": 42,
						},
					},
				],
			},
		],
	}

	assert ast == expected
