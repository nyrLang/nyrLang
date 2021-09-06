import json

from nyr.parser import node
from nyr.parser.parser import Parser


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
			cls=node.ComplexEncoder,
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
			cls=node.ComplexEncoder,
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
												"type": "SuperExpression",
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
													"type": "SuperExpression",
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


def testNewClassInstance():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				class Point3D : Point {
					def Point(x, y, z) {
						super(x, y);
						this.z = z;
					}

					def add() {
						return super() + this.z;
					}
				}

				let cls = Point3D(10, 20, 30);
			"""),
			cls=node.ComplexEncoder,
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
												"type": "SuperExpression",
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
								"name": "add",
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
													"type": "SuperExpression",
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
			{
				"type": "VariableStatement",
				"declarations": [
					{
						"type": "VariableDeclaration",
						"id": {
							"type": "Identifier",
							"name": "cls",
						},
						"init": {
							"type": "CallExpression",
							"callee": {
								"type": "Identifier",
								"name": "Point3D",
							},
							"arguments": [
								{
									"type": "IntegerLiteral",
									"value": 10,
								},
								{
									"type": "IntegerLiteral",
									"value": 20,
								},
								{
									"type": "IntegerLiteral",
									"value": 30,
								},
							],
						},
					},
				],
			},
		],
	}

	assert ast == expected
