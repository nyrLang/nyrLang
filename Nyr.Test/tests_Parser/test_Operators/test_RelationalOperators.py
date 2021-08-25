import json

import pytest

from Nyr.Parser import Node
from Nyr.Parser.Parser import Parser


@pytest.mark.parametrize(
	("operator"), (
		(">"),
		(">="),
		("<"),
		("<="),
	),
)
def testRelationalOperators(operator: str):
	ast = json.loads(
		json.dumps(
			Parser().parse(f"x {operator} 0;"),
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "BinaryExpression",
					"operator": operator,
					"left": {
						"type": "Identifier",
						"name": "x",
					},
					"right": {
						"type": "IntegerLiteral",
						"value": 0,
					},
				},
			},
		],
	}

	assert ast == expected
