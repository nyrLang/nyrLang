import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testWhileStatement():
	ast = Parser().parse("""
		while (x > 10) {
			x -= 1;
		}
	""")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.WhileStatement)

	# DoWhile.test
	test = node.test
	assert isinstance(test, Node.BinaryExpression)
	assert test.operator == ">"

	assert isinstance(test.left, Node.Identifier)
	assert test.left.name == "x"

	assert isinstance(test.right, Node.IntegerLiteral)
	assert test.right.value == 10

	# DoWhile.body
	body = node.body
	assert isinstance(body, Node.BlockStatement)
	assert len(body.body) == 1

	blockBody = body.body[0]
	assert isinstance(blockBody, Node.ExpressionStatement)

	expression = blockBody.expression

	assert isinstance(expression, Node.AssignmentExpression)
	assert expression.operator == "-="

	assert isinstance(expression.left, Node.Identifier)
	assert expression.left.name == "x"

	assert isinstance(expression.right, Node.IntegerLiteral)
	assert expression.right.value == 1


def testDoWhileStatement():
	ast = Parser().parse("""
		do {
			x -= 1;
		} while (x > 10);
	""")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.DoWhileStatement)

	# DoWhile.body
	body = node.body
	assert isinstance(body, Node.BlockStatement)
	assert len(body.body) == 1

	blockBody = body.body[0]
	assert isinstance(blockBody, Node.ExpressionStatement)

	expression = blockBody.expression

	assert isinstance(expression, Node.AssignmentExpression)
	assert expression.operator == "-="

	assert isinstance(expression.left, Node.Identifier)
	assert expression.left.name == "x"

	assert isinstance(expression.right, Node.IntegerLiteral)
	assert expression.right.value == 1

	# DoWhile.test
	test = node.test
	assert isinstance(test, Node.BinaryExpression)
	assert test.operator == ">"

	assert isinstance(test.left, Node.Identifier)
	assert test.left.name == "x"

	assert isinstance(test.right, Node.IntegerLiteral)
	assert test.right.value == 10


class TestForStatement:
	def testFull(self):
		ast = Parser().parse("""
			for (let i = 0; i < 10; i += 1) {
				x += i;
			}
		""")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.ForStatement)

		# ForStatement.init
		init = node.init
		assert isinstance(init, Node.VariableStatement)
		assert len(init.declarations) == 1

		declaration = init.declarations[0]
		assert isinstance(declaration, Node.VariableDeclaration)

		assert isinstance(declaration.id, Node.Identifier)
		assert declaration.id.name == "i"

		assert isinstance(declaration.init, Node.IntegerLiteral)
		assert declaration.init.value == 0

		# ForStatement.test
		test = node.test
		assert isinstance(test, Node.BinaryExpression)
		assert test.operator == "<"

		assert isinstance(test.left, Node.Identifier)
		assert test.left.name == "i"

		assert isinstance(test.right, Node.IntegerLiteral)
		assert test.right.value == 10

		# ForStatement.update
		update = node.update
		assert isinstance(update, Node.AssignmentExpression)
		assert update.operator == "+="

		assert isinstance(update.left, Node.Identifier)
		assert update.left.name == "i"

		assert isinstance(update.right, Node.IntegerLiteral)
		assert update.right.value == 1

		# ForStatement.body
		body = node.body
		assert isinstance(body, Node.BlockStatement)

	def testMissingInit(self):
		ast = Parser().parse("""
			for ( ; i < 10; i += 1) {
				x += i;
			}
		""")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.ForStatement)

		# ForStatement.init
		assert node.init is None

		# ForStatement.test
		test = node.test
		assert isinstance(test, Node.BinaryExpression)
		assert test.operator == "<"

		assert isinstance(test.left, Node.Identifier)
		assert test.left.name == "i"

		assert isinstance(test.right, Node.IntegerLiteral)
		assert test.right.value == 10

		# ForStatement.update
		update = node.update
		assert isinstance(update, Node.AssignmentExpression)
		assert update.operator == "+="

		assert isinstance(update.left, Node.Identifier)
		assert update.left.name == "i"

		assert isinstance(update.right, Node.IntegerLiteral)
		assert update.right.value == 1

		# ForStatement.body
		body = node.body
		assert isinstance(body, Node.BlockStatement)

	def testMissingTest(self):
		ast = Parser().parse("""
			for (let i = 0; ; i += 1) {
				x += i;
			}
		""")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.ForStatement)

		# ForStatement.init
		init = node.init
		assert isinstance(init, Node.VariableStatement)
		assert len(init.declarations) == 1

		declaration = init.declarations[0]
		assert isinstance(declaration, Node.VariableDeclaration)

		assert isinstance(declaration.id, Node.Identifier)
		assert declaration.id.name == "i"

		assert isinstance(declaration.init, Node.IntegerLiteral)
		assert declaration.init.value == 0

		# ForStatement.test
		assert node.test is None

		# ForStatement.update
		update = node.update
		assert isinstance(update, Node.AssignmentExpression)
		assert update.operator == "+="

		assert isinstance(update.left, Node.Identifier)
		assert update.left.name == "i"

		assert isinstance(update.right, Node.IntegerLiteral)
		assert update.right.value == 1

		# ForStatement.body
		body = node.body
		assert isinstance(body, Node.BlockStatement)

	def testMissingUpdate(self):
		ast = Parser().parse("""
			for (let i = 0; i < 10; ) {
				x += i;
			}
		""")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.ForStatement)

		# ForStatement.init
		init = node.init
		assert isinstance(init, Node.VariableStatement)
		assert len(init.declarations) == 1

		declaration = init.declarations[0]
		assert isinstance(declaration, Node.VariableDeclaration)

		assert isinstance(declaration.id, Node.Identifier)
		assert declaration.id.name == "i"

		assert isinstance(declaration.init, Node.IntegerLiteral)
		assert declaration.init.value == 0

		# ForStatement.test
		test = node.test
		assert isinstance(test, Node.BinaryExpression)
		assert test.operator == "<"

		assert isinstance(test.left, Node.Identifier)
		assert test.left.name == "i"

		assert isinstance(test.right, Node.IntegerLiteral)
		assert test.right.value == 10

		# ForStatement.update
		assert node.update is None

		# ForStatement.body
		body = node.body
		assert isinstance(body, Node.BlockStatement)

	def testMissingAll(self):
		ast = Parser().parse("""
			for ( ; ; ) {
				x += i;
			}
		""")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.ForStatement)

		assert node.init is None
		assert node.test is None
		assert node.update is None

		# ForStatement.body
		body = node.body
		assert isinstance(body, Node.BlockStatement)
