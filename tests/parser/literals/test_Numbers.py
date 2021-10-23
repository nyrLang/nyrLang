import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("test"), (
		pytest.param("42;", id="no space"),
		pytest.param("   42;   ", id="space around"),
		pytest.param("42  ;", id="space before semicolon"),
	),
)
def testInteger(test: str):
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
					"type": "IntegerLiteral",
					"value": 42,
				},
			},
		],
	}

	assert ast == expected


@pytest.mark.parametrize(
	("test"), (
		pytest.param("3.141;", id="no space"),
		pytest.param("   3.141;   ", id="space around"),
		pytest.param("3.141  ;", id="space before semicolon"),
	),
)
def testFloat(test: str):
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
