import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


def testEmptyString():
	ast = json.loads(
		json.dumps(
			Parser().parse('"";'),
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
					"value": "",
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.parametrize(
	("test"), (
		pytest.param('"Hello";', id="no space"),
		pytest.param('    "Hello";    ', id="space around"),
		pytest.param('"Hello"  ;', id="space before semicolon"),
	),
)
def testSimpleString(test: str):
	ast = json.loads(
		json.dumps(
			Parser().parse(test),
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
					"value": "Hello",
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.parametrize(
	("test"), (
		pytest.param('"Hello, World";', id="no space"),
		pytest.param('    "Hello, World";    ', id="space around"),
		pytest.param('"Hello, World"  ;', id="space before semicolon"),
	),
)
def testComplexString(test):
	ast = json.loads(
		json.dumps(
			Parser().parse(test),
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
					"value": "Hello, World",
				},
			},
		],
	}

	assert ast == expected


def testUnclosedString():
	with pytest.raises(SyntaxError):
		Parser().parse(r'"Unclosed string ahead!')
