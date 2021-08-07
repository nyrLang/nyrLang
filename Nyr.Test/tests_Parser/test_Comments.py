import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testSingleLineComment():
	ast = Parser().parse("// Single line comment")

	assert len(ast.body) == 0


def testSingleLineCommentWithValue():
	ast = Parser().parse("""
		// Comment
		"value here";
	""")

	body = ast.body

	assert len(body) == 1

	node = body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.Literal)
	assert expression.type == "StringLiteral"
	assert expression.value == "value here"


def testMultiLineComment():
	ast = Parser().parse("""
		/*
			Multi-line
			Comment
		*/
	""")

	assert len(ast.body) == 0


def testMultiLineCommentWithValue():
	ast = Parser().parse("""
		/*
			Multi-line
			Comment
		*/
		3.141;
	""")

	body = ast.body

	assert len(body) == 1

	node = body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.Literal)
	assert expression.type == "FloatLiteral"
	assert expression.value == 3.141
