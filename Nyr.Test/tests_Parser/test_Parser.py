from Nyr.Parser.Parser import Parser


def testParseEmpty():
	ast = Parser().parse("")

	assert len(ast.body) == 0
