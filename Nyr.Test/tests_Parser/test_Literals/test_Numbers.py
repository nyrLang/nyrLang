import json

import pytest

from Nyr.Parser import Node
from Nyr.Parser.Parser import Parser


@pytest.mark.parametrize(
	("test"), (
		("42;"),
		("   42;   "),
		("42  ;"),
	),
)
def testInteger(test: str):
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
					"type": "IntegerLiteral",
					"value": 42,
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.parametrize(
	("test"), (
		("3.141;"),
		("   3.141;   "),
		("3.141  ;"),
	),
)
def testFloat(test: str):
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
					"type": "FloatLiteral",
					"value": 3.141,
				},
			},
		],
	}

	assert ast == expected


def testFloatTooManyDots():
	with pytest.raises(SyntaxError, match='Unexpected end of input, expected "IDENTIFIER"'):
		Parser().parse("3.141.59")
