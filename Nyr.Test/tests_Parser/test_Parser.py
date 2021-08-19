import json

from Nyr.Parser.Node import ComplexEncoder
from Nyr.Parser.Parser import Parser


def testParseEmpty():
	ast = json.loads(
		json.dumps(
			Parser().parse(""),
			cls=ComplexEncoder,
		),
	)

	expected = {
		"type": "Program",
		"body": [],
	}

	assert ast == expected
