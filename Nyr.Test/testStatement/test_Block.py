from Nyr.Parser.Parser import Parser


def test():
	parser = Parser()
	ast = parser.parse("""{
		42;

		"Hello";
	}""")

	assert ast.type == "Program"

	body = ast.body
	assert len(body) == 1
	assert body[0].type == "BlockStatement"

	blockBody = body[0].body
	assert len(blockBody) == 2
	assert blockBody[0].type == "ExpressionStatement"
	assert blockBody[0].expression.type == "NumericLiteral"
	assert blockBody[0].expression.value == 42

	assert blockBody[1].type == "ExpressionStatement"
	assert blockBody[1].expression.type == "StringLiteral"
	assert blockBody[1].expression.value == "Hello"
