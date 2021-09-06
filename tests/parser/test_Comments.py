import json

from nyr.parser import node
from nyr.parser.parser import Parser


def testSingleLineComment():
	ast = json.loads(
		json.dumps(
			Parser().parse("// Single line comment"),
			cls=node.ComplexEncoder,
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
			cls=node.ComplexEncoder,
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
			cls=node.ComplexEncoder,
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
			cls=node.ComplexEncoder,
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
