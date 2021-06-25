import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testBlockStatement():
	parser = Parser()
	ast = parser.parse("""{
		42;

		"Hello";
	}""")

	assert ast.type == "Program"

	body = ast.body
	assert len(body) == 1

	block = body[0]
	assert isinstance(block, Node.BlockStatement), f"{block.type} should be of type {Node.BlockStatement.type}"

	blockBody = block.body

	assert len(blockBody) == 2

	node = blockBody[0]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.IntegerLiteral)
	assert expression.value == 42

	node = blockBody[1]
	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.StringLiteral)
	assert expression.value == "Hello"
