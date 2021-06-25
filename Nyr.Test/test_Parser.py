import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testParseEmpty():
	parser = Parser()

	ast = parser.parse("")

	assert len(ast.body) == 0


def testEmptyStatement():
	parser = Parser()

	ast = parser.parse(";")

	assert len(ast.body) == 1

	assert isinstance(ast.body[0], Node.EmptyStatement)
	assert ast.body[0].type == "EmptyStatement"


class TestParseNumber:
	def testInteger(self):
		parser = Parser()

		for test in ["42;", "   42;   ", "42  ;"]:
			ast = parser.parse(test)

			assert ast.type == "Program"
			body = ast.body

			assert len(body) == 1

			node = body[0]

			if not isinstance(node, Node.ExpressionStatement):
				assert False, f"{node.type} should be of type {Node.ExpressionStatement.type}"

			assert node.type == "ExpressionStatement"

			expression = node.expression

			assert isinstance(expression, Node.IntegerLiteral)

			assert expression.value == 42

	def testFloat(self):
		parser = Parser()

		for test in ["3.141;", "   3.141;   ", "3.141  ;"]:
			ast = parser.parse(test)

			assert ast.type == "Program"
			body = ast.body

			assert len(body) == 1

			node = body[0]

			if not isinstance(node, Node.ExpressionStatement):
				assert False, f"{node.type} should be of type {Node.ExpressionStatement.type}"

			expression = node.expression

			assert isinstance(expression, Node.FloatLiteral)

			assert expression.value == 3.141


class TestParseString:
	def testDoubleQuote(self):
		parser = Parser()

		for test in [r'"Hello";', r'    "Hello";    ', r'"Hello"  ;', r'"Hello, World";', r'   "Hello, World";   ', r'"Hello, World"   ;']:
			ast = parser.parse(test)

			assert ast.type == "Program"
			body = ast.body

			assert len(body) == 1

			node = body[0]

			if not isinstance(node, Node.ExpressionStatement):
				assert False, f"{node.type} should be of type {Node.ExpressionStatement.type}"

			expression = node.expression

			assert isinstance(expression, Node.StringLiteral)
			assert expression.value in ("Hello", "Hello, World")

	def testSingleQuote(self):
		parser = Parser()

		for test in [r"'Hello';", r"   'Hello';   ", r"'Hello'   ;", r"'Hello, World';", r"   'Hello, World';   ", r"'Hello, World'   ;"]:
			ast = parser.parse(test)

			assert ast.type == "Program"
			body = ast.body

			assert len(body) == 1

			node = body[0]

			if not isinstance(node, Node.ExpressionStatement):
				assert False, f"{node.type} should be of type {Node.ExpressionStatement.type}"

			expression = node.expression

			assert isinstance(expression, Node.StringLiteral)
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

		node = body[0]

		if not isinstance(node, Node.ExpressionStatement):
			assert False, f"{node.type} should be of type {Node.ExpressionStatement.type}"

		expression = node.expression

		assert isinstance(expression, Node.StringLiteral)
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
			3.141;
		""")

		body = ast.body

		assert len(body) == 1

		node = body[0]

		if not isinstance(node, Node.ExpressionStatement):
			assert False, f"{node.type} should be of type {Node.ExpressionStatement.type}"

		expression = node.expression

		assert isinstance(expression, Node.FloatLiteral)
		assert expression.value == 3.141
