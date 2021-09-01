import pytest

from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Interpreter.Interpreter import MAXITERATIONS
from Nyr.Parser.Parser import Parser


def testWhileLoop():
	ast = Parser().parse("""
		let x = 0;
		while (x < 5) {
			x += 1;
		}
	""")

	env = Interpreter().interpret(ast)

	assert env == {"x": 5}


def testWhileLoopBreak():
	ast = Parser().parse("""
		let x = 0;
		while (x < 5) {
			x += 1;
			if (x == 2) {
				break;
			}
		}
	""")

	env = Interpreter().interpret(ast)

	assert env == {"x": 2}


def testDoWhile():
	ast = Parser().parse("""
		let x = 0;
		do {
			x += 7;
		} while (false);
	""")

	env = Interpreter().interpret(ast)

	assert env == {"x": 7}


def testDoWhileBreak():
	ast = Parser().parse("""
		let x = 0;
		do {
			x += 1;
			if (x == 9) {
				break;
			}
		} while (true);
	""")

	env = Interpreter().interpret(ast)

	assert env == {"x": 9}


def testForLoop():
	ast = Parser().parse("""
		let x = 0;
		for (let i = 0; i < 10; i += 2) {
			x += i;
		}

		let y = 0;
		let i = 7;
		for (i = 0; i < 10; i += 2) {
			y += i;
		}
	""")

	env = Interpreter().interpret(ast)

	assert env == {"i": 10, "x": 20, "y": 20}


def testForLoopBreak():
	ast = Parser().parse("""
		let x = 0;
		for (let i = 0; ; i += 2) {
			x += i;
			if (i == 6) {
				break;
			}
		}

		let y = 0;
		let i = 7;
		for (i = 0; i < 10; i += 2) {
			y += i;
		}
	""")

	env = Interpreter().interpret(ast)

	assert env == {"i": 10, "x": 12, "y": 20}


@pytest.mark.parametrize(
	("loop", "type_"), (
		("for (;;) { }", "for"),
		("while (true) { }", "while"),
		("do { } while (true);", "do-while"),
	),
)
def testIterationOverflow(loop: str, type_: str):
	# Iterate forever
	ast = Parser().parse(loop)

	with pytest.raises(Exception, match=f"Exceeded {MAXITERATIONS} iterations in {type_} statement"):
		Interpreter().interpret(ast)
