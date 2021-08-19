import json

import pytest

import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


@pytest.mark.parametrize(
	("operator"), (
		("+"),
		("-"),
		("!"),
	),
)
def testUnary(operator: str):
	ast = json.loads(
		json.dumps(
			Parser().parse(f"{operator}x;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "UnaryExpression",
					"operator": operator,
					"argument": {
						"type": "Identifier",
						"name": "x",
					},
				},
			},
		],
	}

	assert ast == expected
