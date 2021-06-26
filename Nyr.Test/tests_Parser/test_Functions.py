import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


class TestFunctionDeclarations:
	def testEmptyBody(self):
		ast = Parser().parse("def square() { } ")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.FunctionDeclaration)
		assert node.name.name == "square"

		assert len(node.params) == 0

		assert isinstance(node.body, Node.BlockStatement)

		assert len(node.body.body) == 0

	def testWithoutArgs(self):
		ast = Parser().parse("""
			def square() {
				return;
			}
		""")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.FunctionDeclaration)
		assert node.name.name == "square"

		assert len(node.params) == 0

		assert isinstance(node.body, Node.BlockStatement)

		ret = node.body.body[0]
		assert isinstance(ret, Node.ReturnStatement)

		assert ret.argument is None

	def testWithSingleArg(self):
		ast = Parser().parse("""
			def square(x) {
				return x * x;
			}
		""")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.FunctionDeclaration)
		assert node.name.name == "square"

		assert len(node.params) == 1

		param = node.params[0]
		assert isinstance(param, Node.Identifier)
		assert param.name == "x"

		assert isinstance(node.body, Node.BlockStatement)

		body = node.body.body[0]
		assert isinstance(body, Node.ReturnStatement)

		expression = body.argument
		assert isinstance(expression, Node.ComplexExpression)

		assert expression.type == "BinaryExpression"
		assert expression.operator == "*"

		assert isinstance(expression.left, Node.Identifier)
		assert expression.left.name == "x"

		assert isinstance(expression.right, Node.Identifier)
		assert expression.right.name == "x"

	def testWithMultipleArgs(self):
		ast = Parser().parse("""
			def sum(x, y) {
				return x + y;
			}
		""")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.FunctionDeclaration)
		assert node.name.name == "sum"

		assert len(node.params) == 2

		param1 = node.params[0]
		assert isinstance(param1, Node.Identifier)
		assert param1.name == "x"

		param2 = node.params[1]
		assert isinstance(param2, Node.Identifier)
		assert param2.name == "y"

		assert isinstance(node.body, Node.BlockStatement)

		body = node.body.body[0]
		assert isinstance(body, Node.ReturnStatement)

		expression = body.argument
		assert isinstance(expression, Node.ComplexExpression)

		assert expression.type == "BinaryExpression"
		assert expression.operator == "+"

		assert isinstance(expression.left, Node.Identifier)
		assert expression.left.name == "x"

		assert isinstance(expression.right, Node.Identifier)
		assert expression.right.name == "y"


class TestFunctionCalls:
	def testSimpleFunctionCall(self):
		ast = Parser().parse("foo(x);")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.ExpressionStatement)

		expression = node.expression
		assert isinstance(expression, Node.CallExpression)

		assert isinstance(expression.callee, Node.Identifier)
		assert expression.callee.name == "foo"

		assert len(expression.arguments) == 1

		arg0 = expression.arguments[0]
		assert isinstance(arg0, Node.Identifier)
		assert arg0.name == "x"

	def testChainedFunctionCall(self):
		ast = Parser().parse("foo(x)();")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.ExpressionStatement)

		expression = node.expression
		assert isinstance(expression, Node.CallExpression)

		assert len(expression.arguments) == 0
		assert isinstance(expression.callee, Node.CallExpression)

		assert isinstance(expression.callee.callee, Node.Identifier)
		assert expression.callee.callee.name == "foo"

		assert len(expression.callee.arguments) == 1

		arg = expression.callee.arguments[0]
		assert isinstance(arg, Node.Identifier)
		assert arg.name == "x"

	def testMemberFunctionCall(self):
		ast = Parser().parse("system.print(x, y);")

		assert len(ast.body) == 1

		node = ast.body[0]
		assert isinstance(node, Node.ExpressionStatement)

		expression = node.expression
		assert isinstance(expression, Node.CallExpression)

		assert isinstance(expression.callee, Node.MemberExpression)
		assert expression.callee.computed is False

		assert isinstance(expression.callee.object, Node.Identifier)
		assert expression.callee.object.name == "system"

		assert isinstance(expression.callee.property, Node.Identifier)
		assert expression.callee.property.name == "print"

		assert len(expression.arguments) == 2

		arg0 = expression.arguments[0]
		arg1 = expression.arguments[1]

		assert isinstance(arg0, Node.Identifier)
		assert arg0.name == "x"

		assert isinstance(arg1, Node.Identifier)
		assert arg1.name == "y"

	def testNestedFunctionCall(self):
		ast = Parser().parse("foo(foo(x));")

		assert len(ast.body) == 1

		node = ast.body[0]

		assert isinstance(node, Node.ExpressionStatement)

		expression = node.expression
		assert isinstance(expression, Node.CallExpression)

		assert isinstance(expression.callee, Node.Identifier)
		assert expression.callee.name == "foo"

		assert len(expression.arguments) == 1

		arg0 = expression.arguments[0]
		assert isinstance(arg0, Node.CallExpression)

		assert isinstance(arg0.callee, Node.Identifier)
		assert arg0.callee.name == "foo"

		assert len(arg0.arguments) == 1

		arg1 = arg0.arguments[0]
		assert isinstance(arg1, Node.Identifier)
		assert arg1.name == "x"
