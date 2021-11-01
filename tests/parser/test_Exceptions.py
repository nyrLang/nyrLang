import pytest

from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("code"), (
		pytest.param("42", id="int"),
		pytest.param("3.141", id="float"),
		pytest.param('"Hello, World"', id="string"),
	),
)
def testMissingSemicolon(code: str):
	parser = Parser()

	# FIXME: get a better exception message
	with pytest.raises(Exception, match='Unexpected end of input, expected ";"'):
		parser.parse(code)
