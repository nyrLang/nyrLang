from Nyr.Node import Node
from Nyr.Parser import Parser


class TestParseNumber:
	def testInteger(self):
		parser = Parser()

		for test in ["42;", "   42;   ", "42  ;"]:
			ast = parser.parse(test)

			assert ast["type"] == Node.Program

			body = ast["body"]

			assert len(body) == 1

			assert body[0]["type"] == Node.ExpressionStatement

			assert body[0]["expression"]["type"] == Node.IntegerLiteral
			assert body[0]["expression"]["value"] == 42

	def testFloat(self):
		parser = Parser()

		for test in ["42.5;", "   42.5;   ", "42.5  ;"]:
			ast = parser.parse(test)

			assert ast["type"] == Node.Program

			body = ast["body"]

			assert len(body) == 1

			assert body[0]["type"] == Node.ExpressionStatement

			assert body[0]["expression"]["type"] == Node.FloatLiteral
			assert body[0]["expression"]["value"] == 42.5


class TestParseString:
	def testDoubleQuote(self):
		parser = Parser()

		for test in [r'"Hello";', r'    "Hello";    ', r'"Hello"  ;', r'"Hello, World";', r'   "Hello, World";   ', r'"Hello, World"   ;']:
			ast = parser.parse(test)

			assert ast["type"] == Node.Program

			body = ast["body"]

			assert len(body) == 1

			assert body[0]["type"] == Node.ExpressionStatement
			assert body[0]["expression"]["type"] == Node.StringLiteral
			assert body[0]["expression"]["value"] in ("Hello", "Hello, World")

	def testSingleQuote(self):
		parser = Parser()

		for test in [r"'Hello';", r"   'Hello';   ", r"'Hello'   ;", r"'Hello, World';", r"   'Hello, World';   ", r"'Hello, World'   ;"]:
			ast = parser.parse(test)

			assert ast["type"] == Node.Program

			body = ast["body"]

			assert len(body) == 1

			assert body[0]["type"] == Node.ExpressionStatement
			assert body[0]["expression"]["type"] == Node.StringLiteral
			assert body[0]["expression"]["value"] in ("Hello", "Hello, World")


class TestParseComments:
	def testSingleLineComment(self):
		parser = Parser()
		ast = parser.parse("// Single line comment")

		assert len(ast["body"]) == 0

	def testSingleLineCommentWithValue(self):
		parser = Parser()
		ast = parser.parse("""
			// Comment
			"value here";
		""")

		body = ast["body"]

		assert len(body) == 1

		assert body[0]["type"] == Node.ExpressionStatement
		expression = body[0]["expression"]
		assert expression["type"] == Node.StringLiteral
		assert expression["value"] == "value here"

	def testMultiLineComment(self):
		parser = Parser()
		ast = parser.parse("""
			/*
				Multi-line
				Comment
			*/
		""")

		assert len(ast["body"]) == 0

	def testMultiLineCommentWithValue(self):
		parser = Parser()
		ast = parser.parse("""
			/*
				Multi-line
				Comment
			*/
			3.141;
		""")

		body = ast["body"]

		assert len(body) == 1

		assert body[0]["type"] == Node.ExpressionStatement
		expression = body[0]["expression"]
		assert expression["type"] == Node.FloatLiteral
		assert expression["value"] == 3.141
