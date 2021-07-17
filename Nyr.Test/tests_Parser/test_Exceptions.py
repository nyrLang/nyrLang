import pytest

from Nyr.Parser.Parser import Parser


def testMissingSemicolon():
	parser = Parser()

	for test in ["42", "3.141", r'"Hello, World"']:
		with pytest.raises(Exception):
			parser.parse(test)
