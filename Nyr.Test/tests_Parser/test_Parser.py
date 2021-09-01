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


def testParseMultiple():
	parser = Parser()

	for i in range(10):
		ast = json.loads(
			json.dumps(
				parser.parse(f"let x = {i};"),
				cls=ComplexEncoder,
			),
		)

		assert ast == {
			"type": "Program",
			"body": [
				{
					"type": "VariableStatement",
					"declarations": [
						{
							"type": "VariableDeclaration",
							"id": {
								"type": "Identifier",
								"name": "x",
							},
							"init": {
								"type": "IntegerLiteral",
								"value": i,
							},
						},
					],
				},
			],
		}
