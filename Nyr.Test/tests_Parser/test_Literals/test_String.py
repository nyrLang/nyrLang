import json

import pytest

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testEmptyString():
	ast = json.loads(
		json.dumps(
			Parser().parse('"";'),
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
					"value": "",
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.parametrize(
	("test"), [
		(r'"Hello";'),
		(r'    "Hello";    '),
		(r'"Hello"  ;'),
	],
)
def testSimpleString(test: str):
	ast = json.loads(
		json.dumps(
			Parser().parse(test),
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
		],
	}

	assert ast == expected


@pytest.mark.parametrize(
	("test"), [
		(r'"Hello, World";'),
		(r'    "Hello, World";    '),
		(r'"Hello, World"  ;'),
	],
)
def testComplexString(test):
	ast = json.loads(
		json.dumps(
			Parser().parse(test),
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
					"value": "Hello, World",
				},
			},
		],
	}

	assert ast == expected


def testUnclosedString():
	with pytest.raises(Exception):
		Parser().parse(r'"Unclosed string ahead!')
