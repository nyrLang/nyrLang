import json

import pytest

from Nyr.Parser import Node
from Nyr.Parser.Parser import Parser


@pytest.mark.parametrize(
	("operator"), (
		("&&"),
		("||"),
	),
)
def testLogicalOperatorsP(operator: str):
	ast = json.loads(
		json.dumps(
			Parser().parse(f"x >= 5 {operator} y <= 20;"),
			cls=Node.ComplexEncoder,
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
