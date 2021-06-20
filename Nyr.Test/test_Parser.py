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

			assert body[0]["expression"]["type"] == Node.NumericLiteral
			assert body[0]["expression"]["value"] == 42


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

# TODO: Test throw error with "Missing ';'"
# class TestParseComments:
# 	def testSingleLineComment(self):
# 		parser = Parser()
# 		ast = parser.parse("// Single line comment")
#
# 	def testMultiLineComment(self):
# 		parser = Parser()
# 		ast = parser.parse("""
# /*
# 	Multi-line
# 	Comment
# 	*/
# """)
