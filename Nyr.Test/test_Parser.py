from Nyr.Node import Node
from Nyr.Parser import Parser


class TestParseNumber:
	def testInteger(self):
		parser = Parser()
		ast = parser.parse("42;")

		assert ast.get("type") == Node.Program

		assert len(ast.get("body")) == 1

		assert ast.get("body")[0].get("type") == Node.ExpressionStatement

		assert ast.get("body")[0].get("expression").get("type") == Node.NumericLiteral
		assert ast.get("body")[0].get("expression").get("value") == 42

	def testIntegerWithPadding(self):
		parser = Parser()
		ast = parser.parse("   42;   ")

		assert ast.get("type") == Node.Program

		assert len(ast.get("body")) == 1

		assert ast.get("body")[0].get("type") == Node.ExpressionStatement

		assert ast.get("body")[0].get("expression").get("type") == Node.NumericLiteral
		assert ast.get("body")[0].get("expression").get("value") == 42

	def testIntegerSpaceBeforeSemicolon(self):
		parser = Parser()
		ast = parser.parse("42   ;")

		assert ast.get("type") == Node.Program

		assert len(ast.get("body")) == 1

		assert ast.get("body")[0].get("type") == Node.ExpressionStatement

		assert ast.get("body")[0].get("expression").get("type") == Node.NumericLiteral
		assert ast.get("body")[0].get("expression").get("value") == 42


class TestParseString:
	# Double Quotes ( " )
	class TestDoubleQuote:
		def test(self):
			parser = Parser()
			ast = parser.parse(r'"Hello";')

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello"

		def testWithPadding(self):
			parser = Parser()
			ast = parser.parse(r'    "Hello";    ')

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello"

		def testWithSpaces(self):
			parser = Parser()
			ast = parser.parse(r'"Hello, World";')

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello, World"

		def testWithSpacesAndPadding(self):
			parser = Parser()
			ast = parser.parse(r'   "Hello, World";   ')

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello, World"

		def testWithSpaceBeforeSemicolon(self):
			parser = Parser()
			ast = parser.parse(r'"Hello"  ;')

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello"

		def testWithSpacesAndSpaceBeforeSemicolon(self):
			parser = Parser()
			ast = parser.parse(r'"Hello, World"   ;')

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello, World"

	# Singe Quotes ( ' )
	class TestSingleQuote:
		def test(self):
			parser = Parser()
			ast = parser.parse(r"'Hello';")

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello"

		def testWithPadding(self):
			parser = Parser()
			ast = parser.parse(r"   'Hello';   ")

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello"

		def testWithSpaces(self):
			parser = Parser()
			ast = parser.parse(r"'Hello, World';")

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello, World"

		def testSpacesAndPadding(self):
			parser = Parser()
			ast = parser.parse(r"   'Hello, World';   ")

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello, World"

		def testWithSpaceBeforeSemicolon(self):
			parser = Parser()
			ast = parser.parse(r"'Hello'   ;")

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello"

		def testWithSpacesAndSpaceBeforeSemicolon(self):
			parser = Parser()
			ast = parser.parse(r"'Hello, World'   ;")

			assert ast.get("type") == Node.Program

			assert len(ast.get("body")) == 1

			assert ast.get("body")[0].get("type") == Node.ExpressionStatement
			assert ast.get("body")[0].get("expression").get("type") == Node.StringLiteral
			assert ast.get("body")[0].get("expression").get("value") == "Hello, World"


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
