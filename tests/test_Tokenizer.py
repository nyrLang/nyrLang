import pytest

from nyr.parser.tokenizer import Token
from nyr.parser.tokenizer import Tokenizer


def testEmptyInput():
	t = Tokenizer()
	t.init("")
	tks = t.getTokens()

	assert len(tks) == 1
	assert tks[0].type == "EOF"


@pytest.mark.parametrize(
	("code"), (
		pytest.param(
			"// This is a comment",
			id="single-line comment",
		),
		pytest.param(
			"""
			/*
				This is a
				multiline
				comment
			*/
			""",
			id="multi-line comment",
		),
	),
)
def testCommentInput(code: str):
	t = Tokenizer()
	t.init(code)
	tks = t.getTokens()

	assert len(tks) == 1
	assert tks[0].type == "EOF"


def testInput():
	t = Tokenizer()
	t.init("let x, y; foo()")
	tks = t.getTokens()
	expected = (
		Token("let", "let"),
		Token("IDENTIFIER", "x"),
		Token(",", ","),
		Token("IDENTIFIER", "y"),
		Token(";", ";"),
		Token("IDENTIFIER", "foo"),
		Token("(", "("),
		Token(")", ")"),
		Token("EOF", None),
	)

	assert len(tks) == 9
	for i in range(9):
		assert tks[i].type == expected[i].type
		assert tks[i].value == expected[i].value


def testTokenRepr():
	assert repr(Token("EOF", None)) == f"nyr.parser.tokenizer.Token('EOF')"
