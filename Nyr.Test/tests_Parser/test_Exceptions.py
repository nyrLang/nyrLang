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

	with pytest.raises(Exception):
		parser.parse(code)
