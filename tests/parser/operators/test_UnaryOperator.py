import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


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
			cls=node.ComplexEncoder,
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
