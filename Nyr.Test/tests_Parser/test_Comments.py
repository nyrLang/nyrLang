import json

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testSingleLineComment():
	ast = json.loads(
		json.dumps(
			Parser().parse("// Single line comment"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [],
	}

	assert ast == expected


def testSingleLineCommentWithValue():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				// Comment
				"value here";
			"""),
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
					"value": "value here",
				},
			},
		],
	}

	assert ast == expected


def testMultiLineComment():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				/*
					Multi-line
					Comment
				*/
			"""),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [],
	}

	assert ast == expected


def testMultiLineCommentWithValue():
	ast = json.loads(
		json.dumps(
			Parser().parse("""
				/*
					Multi-line
					Comment
				*/
				3.141;
			"""),
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
		],
	}

	assert ast == expected
