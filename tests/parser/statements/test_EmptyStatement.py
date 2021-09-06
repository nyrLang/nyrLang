import json

import pytest

from nyr.parser import node
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("code", "expectedBody"), (
		(";", [{"type": "EmptyStatement"}]),
		(";;", [{"type": "EmptyStatement"}, {"type": "EmptyStatement"}]),
		(";;;", [{"type": "EmptyStatement"}, {"type": "EmptyStatement"}, {"type": "EmptyStatement"}]),
	),
)
def testEmptyStatement(code: str, expectedBody):
	ast = json.loads(
		json.dumps(
			Parser().parse(code),
			cls=node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": expectedBody,
	}

	assert ast == expected
