import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("operator"), (
		(r"^"),
		(r"|"),
		(r"&"),
	),
)
def testBitwiseOperatorP(operator: str):
	ast = json.loads(
		json.dumps(
			Parser().parse(f"true {operator} false;"),
			cls=node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [
			{
				"type": "ExpressionStatement",
				"expression": {
					"type": "BitwiseExpression",
					"operator": operator,
					"left": {
						"type": "BooleanLiteral",
						"value": True,
					},
					"right": {
						"type": "BooleanLiteral",
						"value": False,
					},
				},
			},
		],
	}

	assert ast == expected
