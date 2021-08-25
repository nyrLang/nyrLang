import json

import pytest

from Nyr.Parser import Node
from Nyr.Parser.Parser import Parser


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
			cls=Node.ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": expectedBody,
	}

	assert ast == expected
