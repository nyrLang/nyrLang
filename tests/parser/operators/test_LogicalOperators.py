import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("operator"), (
		pytest.param("&&", id="logical and"),
		pytest.param("||", id="logical or"),
	),
)
def testLogicalOperatorsP(operator: str):
	ast = json.loads(
		json.dumps(
			Parser().parse(f"x >= 5 {operator} y <= 20;"),
			cls=node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "LogicalExpression",
					"operator": operator,
					"left": {
						"type": "BinaryExpression",
						"operator": ">=",
						"left": {
							"type": "Identifier",
							"name": "x",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 5,
						},
					},
					"right": {
						"type": "BinaryExpression",
						"operator": "<=",
						"left": {
							"type": "Identifier",
							"name": "y",
						},
						"right": {
							"type": "IntegerLiteral",
							"value": 20,
						},
					},
				},
			},
		],
	}

	assert ast == expected
