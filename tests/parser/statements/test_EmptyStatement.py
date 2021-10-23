import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("code", "expectedCount"), (
		pytest.param(";", 1, id="1"),
		pytest.param(";;", 2, id="2"),
		pytest.param(";;;", 3, id="3"),
	),
)
def testEmptyStatement(code: str, expectedCount: int):
	ast = json.loads(
		json.dumps(
			Parser().parse(code),
			cls=node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [{"type": "EmptyStatement"} for _ in range(expectedCount)],
	}

	assert ast == expected
