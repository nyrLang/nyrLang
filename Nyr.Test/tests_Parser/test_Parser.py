from Nyr.Parser.Parser import Parser


def testParseEmpty():
	parser = Parser()

	ast = parser.parse("")

	assert len(ast.body) == 0
