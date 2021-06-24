import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testParseEmpty():
	parser = Parser()

	ast = parser.parse("")

	assert len(ast.body) == 0


class TestParseNumber:
	def testInteger(self):
		parser = Parser()

		for test in ["42;", "   42;   ", "42  ;"]:
			ast = parser.parse(test)

			assert ast.type == "Program"
			body = ast.body

			assert len(body) == 1

			assert body[0].type == "ExpressionStatement"

			expression: Node.Node = body[0].expression

			assert expression.type == "NumericLiteral"
			assert expression.value == 42


class TestParseString:
	def testDoubleQuote(self):
		parser = Parser()

		for test in [r'"Hello";', r'    "Hello";    ', r'"Hello"  ;', r'"Hello, World";', r'   "Hello, World";   ', r'"Hello, World"   ;']:
			ast = parser.parse(test)

			assert ast.type == "Program"
			body = ast.body

			assert len(body) == 1

			assert body[0].type == "ExpressionStatement"

			expression: Node.Node = body[0].expression

			assert expression.type == "StringLiteral"
			assert expression.value in ("Hello", "Hello, World")

	def testSingleQuote(self):
		parser = Parser()

		for test in [r"'Hello';", r"   'Hello';   ", r"'Hello'   ;", r"'Hello, World';", r"   'Hello, World';   ", r"'Hello, World'   ;"]:
			ast = parser.parse(test)

			assert ast.type == "Program"
			body = ast.body

			assert len(body) == 1

			assert body[0].type == "ExpressionStatement"

			expression: Node.Node = body[0].expression

			assert expression.type == "StringLiteral"
			assert expression.value in ("Hello", "Hello, World")


class TestParseComments:
	def testSingleLineComment(self):
		parser = Parser()
		ast = parser.parse("// Single line comment")

		assert len(ast.body) == 0

	def testSingleLineCommentWithValue(self):
		parser = Parser()
		ast = parser.parse("""
			// Comment
			"value here";
		""")

		body = ast.body

		assert len(body) == 1

		assert body[0].type == "ExpressionStatement"

		expression: Node.Node = body[0].expression

		assert expression.type == "StringLiteral"
		assert expression.value == "value here"

	def testMultiLineComment(self):
		parser = Parser()
		ast = parser.parse("""
			/*
				Multi-line
				Comment
			*/
		""")

		assert len(ast.body) == 0

	def testMultiLineCommentWithValue(self):
		parser = Parser()
		ast = parser.parse("""
			/*
				Multi-line
				Comment
			*/
			3141;
		""")

		body = ast.body

		assert len(body) == 1

		assert body[0].type == "ExpressionStatement"

		expression: Node.Node = body[0].expression

		assert expression.type == "NumericLiteral"
		assert expression.value == 3141
