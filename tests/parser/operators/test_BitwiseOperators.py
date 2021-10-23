import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("operator"), (
		pytest.param(r"^", id="bitwise xor"),
		pytest.param(r"|", id="bitwise or"),
		pytest.param(r"&", id="bitwise and"),
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
