import pytest

from Nyr.Parser.Parser import Parser


@pytest.mark.parametrize(
	("code"), [
		("42"),
		("3.141"),
		(r'"Hello, World"'),
	],
)
def testMissingSemicolon(code: str):
	parser = Parser()

	# FIXME: get a better exception message
	with pytest.raises(Exception, match='Unexpected end of input, expected ";"'):
		parser.parse(code)
