import json

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


class TestFunctionDeclarations:
	def testEmptyBody(self):
		ast = json.loads(
			json.dumps(
				Parser().parse("def foo() { }"),
				cls=Node.ComplexEncoder,
			),
		)

		expected = {
			"type": "Program",
			"body": [
				{
					"type": "FunctionDeclaration",
					"name": {
						"type": "Identifier",
						"name": "foo",
					},
					"params": [],
					"body": {
						"type": "BlockStatement",
						"body": [],
					},
				},
			],
		}

		assert ast == expected

	def testWithoutArgs(self):
		ast = json.loads(
			json.dumps(
				Parser().parse("def foo() { return; }"),
				cls=Node.ComplexEncoder,
			),
		)

		expected = {
			"type": "Program",
			"body": [
				{
					"type": "FunctionDeclaration",
					"name": {
						"type": "Identifier",
						"name": "foo",
					},
					"params": [],
					"body": {
						"type": "BlockStatement",
						"body": [
							{
								"type": "ReturnStatement",
								"argument": None,
							},
						],
					},
				},
			],
		}

		assert ast == expected

	def testWithSingleArg(self):
		ast = json.loads(
			json.dumps(
				Parser().parse("def square(x) { return x * x; } "),
				cls=Node.ComplexEncoder,
			),
		)

		expected = {
			"type": "Program",
			"body": [
				{
					"type": "FunctionDeclaration",
					"name": {
						"type": "Identifier",
						"name": "square",
					},
					"params": [
						{
							"type": "Identifier",
							"name": "x",
						},
					],
					"body": {
						"type": "BlockStatement",
						"body": [
							{
								"type": "ReturnStatement",
								"argument": {
									"type": "BinaryExpression",
									"operator": "*",
									"left": {
										"type": "Identifier",
										"name": "x",
									},
									"right": {
										"type": "Identifier",
										"name": "x",
									},
								},
							},
						],
					},
				},
			],
		}

		assert ast == expected

	def testWithMultipleArgs(self):
		ast = json.loads(
			json.dumps(
				Parser().parse("def sum(x, y) { return x + y; } "),
				cls=Node.ComplexEncoder,
			),
		)

		expected = {
			"type": "Program",
			"body": [
				{
					"type": "FunctionDeclaration",
					"name": {
						"type": "Identifier",
						"name": "sum",
					},
					"params": [
						{
							"type": "Identifier",
							"name": "x",
						},
						{
							"type": "Identifier",
							"name": "y",
						},
					],
					"body": {
						"type": "BlockStatement",
						"body": [
							{
								"type": "ReturnStatement",
								"argument": {
									"type": "BinaryExpression",
									"operator": "+",
									"left": {
										"type": "Identifier",
										"name": "x",
									},
									"right": {
										"type": "Identifier",
										"name": "y",
									},
								},
							},
						],
					},
				},
			],
		}

		assert ast == expected


class TestFunctionCalls:
	def testSimpleFunctionCall(self):
		ast = json.loads(
			json.dumps(
				Parser().parse("foo(x);"),
				cls=Node.ComplexEncoder,
			),
		)

		expected = {
			"type": "Program",
			"body": [
				{
					"type": "ExpressionStatement",
					"expression": {
						"type": "CallExpression",
						"callee": {
							"type": "Identifier",
							"name": "foo",
						},
						"arguments": [
							{
								"type": "Identifier",
								"name": "x",
							},
						],
					},
				},
			],
		}

		assert ast == expected


	def testChainedFunctionCall(self):
		ast = json.loads(
			json.dumps(
				Parser().parse("foo(x)();"),
				cls=Node.ComplexEncoder,
			),
		)

		expected = {
			"type": "Program",
			"body": [
				{
					"type": "ExpressionStatement",
					"expression": {
						"type": "CallExpression",
						"callee": {
							"type": "CallExpression",
							"callee": {
								"type": "Identifier",
								"name": "foo",
							},
							"arguments": [
								{
									"type": "Identifier",
									"name": "x",
								},
							],
						},
						"arguments": [],
					},
				},
			],
		}

		assert ast == expected

	def testMemberFunctionCall(self):
		ast = json.loads(
			json.dumps(
				Parser().parse("system.print(x, y);"),
				cls=Node.ComplexEncoder,
			),
		)

		expected = {
			"type": "Program",
			"body": [
				{
					"type": "ExpressionStatement",
					"expression": {
						"type": "CallExpression",
						"callee": {
							"type": "MemberExpression",
							"computed": False,
							"object": {
								"type": "Identifier",
								"name": "system",
							},
							"property": {
								"type": "Identifier",
								"name": "print",
							},
						},
						"arguments": [
							{
								"type": "Identifier",
								"name": "x",
							},
							{
								"type": "Identifier",
								"name": "y",
							},
						],
					},
				},
			],
		}

		assert ast == expected

	def testNestedFunctionCall(self):
		ast = json.loads(
			json.dumps(
				Parser().parse("foo(foo(x));"),
				cls=Node.ComplexEncoder,
			),
		)

		expected = {
			"type": "Program",
			"body": [
				{
					"type": "ExpressionStatement",
					"expression": {
						"type": "CallExpression",
						"callee": {
							"type": "Identifier",
							"name": "foo",
						},
						"arguments": [
							{
								"type": "CallExpression",
								"callee": {
									"type": "Identifier",
									"name": "foo",
								},
								"arguments": [
									{
										"type": "Identifier",
										"name": "x",
									},
								],
							},
						],
					},
				},
			],
		}

		assert ast == expected
