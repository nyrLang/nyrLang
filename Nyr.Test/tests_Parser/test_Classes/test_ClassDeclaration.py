import json

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testClassWithMethod():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				class Point {
					def Point(x, y) {
						this.x = x;
						this.y = y;
					}

					def calc() {
						return this.x + this.y;
					}
				}
			"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ClassDeclaration",
				"id": {
					"type": "Identifier",
					"name": "Point",
				},
				"superClass": None,
				"body": {
					"type": "BlockStatement",
					"body": [
						{
							"type": "FunctionDeclaration",
							"name": {
								"type": "Identifier",
								"name": "Point",
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
										"type": "ExpressionStatement",
										"expression": {
											"type": "AssignmentExpression",
											"operator": "=",
											"left": {
												"type": "MemberExpression",
												"computed": False,
												"object": {
													"type": "ThisExpression",
												},
												"property": {
													"type": "Identifier",
													"name": "x",
												},
											},
											"right": {
												"type": "Identifier",
												"name": "x",
											},
										},
									},
									{
										"type": "ExpressionStatement",
										"expression": {
											"type": "AssignmentExpression",
											"operator": "=",
											"left": {
												"type": "MemberExpression",
												"computed": False,
												"object": {
													"type": "ThisExpression",
												},
												"property": {
													"type": "Identifier",
													"name": "y",
												},
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
						{
							"type": "FunctionDeclaration",
							"name": {
								"type": "Identifier",
								"name": "calc",
							},
							"params": [],
							"body": {
								"type": "BlockStatement",
								"body": [
									{
										"type": "ReturnStatement",
										"argument": {
											"type": "BinaryExpression",
											"operator": "+",
											"left": {
												"type": "MemberExpression",
												"computed": False,
												"object": {
													"type": "ThisExpression",
												},
												"property": {
													"type": "Identifier",
													"name": "x",
												},
											},
											"right": {
												"type": "MemberExpression",
												"computed": False,
												"object": {
													"type": "ThisExpression",
												},
												"property": {
													"type": "Identifier",
													"name": "y",
												},
											},
										},
									},
								],
							},
						},
					],
				},
			},
		],
	}

	assert ast == expected


def testClassInheritance():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				class Point3D : Point {
					def Point(x, y, z) {
						super(x, y);
						this.z = z;
					}

					def calc() {
						return super() + this.z;
					}
				}
			"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ClassDeclaration",
				"id": {
					"type": "Identifier",
					"name": "Point3D",
				},
				"superClass": {
					"type": "Identifier",
					"name": "Point",
				},
				"body": {
					"type": "BlockStatement",
					"body": [
						{
							"type": "FunctionDeclaration",
							"name": {
								"type": "Identifier",
								"name": "Point",
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
								{
									"type": "Identifier",
									"name": "z",
								},
							],
							"body": {
								"type": "BlockStatement",
								"body": [
									{
										"type": "ExpressionStatement",
										"expression": {
											"type": "CallExpression",
											"callee": {
												"type": "Super",
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
									{
										"type": "ExpressionStatement",
										"expression": {
											"type": "AssignmentExpression",
											"operator": "=",
											"left": {
												"type": "MemberExpression",
												"computed": False,
												"object": {
													"type": "ThisExpression",
												},
												"property": {
													"type": "Identifier",
													"name": "z",
												},
											},
											"right": {
												"type": "Identifier",
												"name": "z",
											},
										},
									},
								],
							},
						},
						{
							"type": "FunctionDeclaration",
							"name": {
								"type": "Identifier",
								"name": "calc",
							},
							"params": [],
							"body": {
								"type": "BlockStatement",
								"body": [
									{
										"type": "ReturnStatement",
										"argument": {
											"type": "BinaryExpression",
											"operator": "+",
											"left": {
												"type": "CallExpression",
												"callee": {
													"type": "Super",
												},
												"arguments": [],
											},
											"right": {
												"type": "MemberExpression",
												"computed": False,
												"object": {
													"type": "ThisExpression",
												},
												"property": {
													"type": "Identifier",
													"name": "z",
												},
											},
										},
									},
								],
							},
						},
					],
				},
			},
		],
	}

	assert ast == expected
