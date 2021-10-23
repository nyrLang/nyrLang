import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("operator"), (
		pytest.param(">", id="greater"),
		pytest.param(">=", id="greater or equal"),
		pytest.param("<", id="less"),
		pytest.param("<=", id="less or equal"),
	),
)
def testRelationalOperators(operator: str):
	ast = json.loads(
		json.dumps(
			Parser().parse(f"x {operator} 0;"),
			cls=node.ComplexEncoder,
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
