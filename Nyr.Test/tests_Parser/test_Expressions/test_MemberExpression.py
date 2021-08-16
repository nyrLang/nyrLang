import json

import pytest

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


@pytest.mark.dependency()
def testSimplePropertyAccess():
	ast = json.loads(
		json.dumps(
			Parser().parse("x.y;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "MemberExpression",
					"computed": False,
					"object": {
						"type": "Identifier",
						"name": "x",
					},
					"property": {
						"type": "Identifier",
						"name": "y",
					},
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.dependency(depends=["testSimplePropertyAccess"])
def testSimplePropertyAssign():
	ast = json.loads(
		json.dumps(
			Parser().parse("x.y = 1;"),
			cls=Node.ComplexEncoder,
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
						"type": "MemberExpression",
						"computed": False,
						"object": {
							"type": "Identifier",
							"name": "x",
						},
						"property": {
							"type": "Identifier",
							"name": "y",
						},
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 1,
					},
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.dependency()
def testComputedPropertyAccess():
	ast = json.loads(
		json.dumps(
			Parser().parse("x[0];"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "MemberExpression",
					"computed": True,
					"object": {
						"type": "Identifier",
						"name": "x",
					},
					"property": {
						"type": "IntegerLiteral",
						"value": 0,
					},
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.dependency(depends=["testComputedPropertyAccess"])
def testComputedPropertyAssign():
	ast = json.loads(
		json.dumps(
			Parser().parse("x[0] = 1;"),
			cls=Node.ComplexEncoder,
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
						"type": "MemberExpression",
						"computed": True,
						"object": {
							"type": "Identifier",
							"name": "x",
						},
						"property": {
							"type": "IntegerLiteral",
							"value": 0,
						},
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 1,
					},
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.dependency()
@pytest.mark.dependency(depends=["testSimplePropertyAccess", "testComputedPropertyAccess"])
def testChainedAndMixedPropertyAccess():
	ast = json.loads(
		json.dumps(
			Parser().parse('a.b.c["d"];'),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "MemberExpression",
					"computed": True,
					"object": {
						"type": "MemberExpression",
						"computed": False,
						"object": {
							"type": "MemberExpression",
							"computed": False,
							"object": {
								"type": "Identifier",
								"name": "a",
							},
							"property": {
								"type": "Identifier",
								"name": "b",
							},
						},
						"property": {
							"type": "Identifier",
							"name": "c",
						},
					},
					"property": {
						"type": "StringLiteral",
						"value": "d",
					},
				},
			},
		],
	}

	assert ast == expected



@pytest.mark.dependency(depends=["testSimplePropertyAssign", "testComputedPropertyAssign", "testChainedAndMixedPropertyAccess"])
def testChainedAndMixedPropertyAssign():
	ast = json.loads(
		json.dumps(
			Parser().parse('a.b.c["d"] = 1;'),
			cls=Node.ComplexEncoder,
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
						"type": "MemberExpression",
						"computed": True,
						"object": {
							"type": "MemberExpression",
							"computed": False,
							"object": {
								"type": "MemberExpression",
								"computed": False,
								"object": {
									"type": "Identifier",
									"name": "a",
								},
								"property": {
									"type": "Identifier",
									"name": "b",
								},
							},
							"property": {
								"type": "Identifier",
								"name": "c",
							},
						},
						"property": {
							"type": "StringLiteral",
							"value": "d",
						},
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 1,
					},
				},
			},
		],
	}

	assert ast == expected
