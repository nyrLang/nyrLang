import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testClassWithMethod():
	ast = Parser().parse("""
		class Point {
			def Point(x, y) {
				this.x = x;
				this.y = y;
			}

			def calc() {
				return this.x + this.y;
			}
		}
	""")

	assert len(ast.body) == 1

	node = ast.body[0]

	# class Point
	assert isinstance(node, Node.ClassDeclaration)

	assert isinstance(node.id, Node.Identifier)
	assert node.id.name == "Point"

	assert node.superClass is None

	# {
	assert isinstance(node.body, Node.BlockStatement)
	assert len(node.body.body) == 2

	# def Point(x, y)
	body_0 = node.body.body[0]
	assert isinstance(body_0, Node.FunctionDeclaration)
	assert body_0.name.name == "Point"
	assert len(body_0.params) == 2

	param_0_0 = body_0.params[0]
	assert isinstance(param_0_0, Node.Identifier)
	assert param_0_0.name == "x"

	param_0_1 = body_0.params[1]
	assert isinstance(param_0_1, Node.Identifier)
	assert param_0_1.name == "y"

	# {
	assert isinstance(body_0.body, Node.BlockStatement)
	assert len(body_0.body.body) == 2

	# this.x = x;
	e = body_0.body.body[0]
	assert isinstance(e, Node.ExpressionStatement)
	body_0_0 = e.expression
	assert isinstance(body_0_0, Node.ComplexExpression)
	assert body_0_0.type == "AssignmentExpression"
	assert body_0_0.operator == "="

	# this.x
	assert isinstance(body_0_0.left, Node.MemberExpression)
	assert body_0_0.left.computed is False
	assert isinstance(body_0_0.left.object, Node.ThisExpression)
	assert isinstance(body_0_0.left.property, Node.Identifier)
	assert body_0_0.left.property.name == "x"

	# = x;
	assert isinstance(body_0_0.right, Node.Identifier)
	assert body_0_0.right.name == "x"

	# this.y = y;
	e = body_0.body.body[1]
	assert isinstance(e, Node.ExpressionStatement)
	body_0_1 = e.expression
	assert isinstance(body_0_1, Node.ComplexExpression)
	assert body_0_1.type == "AssignmentExpression"
	assert body_0_1.operator == "="

	# this.y
	assert isinstance(body_0_1.left, Node.MemberExpression)
	assert body_0_1.left.computed is False
	assert isinstance(body_0_1.left.object, Node.ThisExpression)
	assert isinstance(body_0_1.left.property, Node.Identifier)
	assert body_0_1.left.property.name == "y"

	# = y;
	assert isinstance(body_0_1.right, Node.Identifier)
	assert body_0_1.right.name == "y"
	# }

	# def calc()
	body_1 = node.body.body[1]
	assert isinstance(body_1, Node.FunctionDeclaration)
	assert body_1.name.name == "calc"
	assert len(body_1.params) == 0

	# {
	assert isinstance(body_1.body, Node.BlockStatement)
	assert len(body_1.body.body) == 1

	# return this.x + this.y;
	body_1_0 = body_1.body.body[0]
	assert isinstance(body_1_0, Node.ReturnStatement)
	assert isinstance(body_1_0.argument, Node.ComplexExpression)

	# this.x + this.y;
	assert body_1_0.argument.type == "BinaryExpression"
	assert body_1_0.argument.operator == "+"

	# this.x
	assert isinstance(body_1_0.argument.left, Node.MemberExpression)
	assert body_1_0.argument.left.computed is False

	# this
	assert isinstance(body_1_0.argument.left.object, Node.ThisExpression)

	# x
	assert isinstance(body_1_0.argument.left.property, Node.Identifier)
	assert body_1_0.argument.left.property.name == "x"

	# this.y
	assert isinstance(body_1_0.argument.right, Node.MemberExpression)
	assert body_1_0.argument.right.computed is False

	# this
	assert isinstance(body_1_0.argument.right.object, Node.ThisExpression)

	# y
	assert isinstance(body_1_0.argument.right.property, Node.Identifier)
	assert body_1_0.argument.right.property.name == "y"


def testClassInheritance():
	ast = Parser().parse("""
		class Point3D : Point {
			def Point(x, y, z) {
				super(x, y);
				this.z = z;
			}

			def calc() {
				return super() + this.z;
			}
		}
	""")

	assert len(ast.body) == 1

	node = ast.body[0]

	# class Point
	assert isinstance(node, Node.ClassDeclaration)

	assert isinstance(node.id, Node.Identifier)
	assert node.id.name == "Point3D"

	assert isinstance(node.superClass, Node.Identifier)
	assert node.superClass.name == "Point"

	assert isinstance(node.body, Node.BlockStatement)
	assert len(node.body.body) == 2

	# def Point(x, y, z)
	body_0 = node.body.body[0]
	assert isinstance(body_0, Node.FunctionDeclaration)
	assert body_0.name.name == "Point"
	assert len(body_0.params) == 3

	param_0_0 = body_0.params[0]
	assert isinstance(param_0_0, Node.Identifier)
	assert param_0_0.name == "x"

	param_0_1 = body_0.params[1]
	assert isinstance(param_0_1, Node.Identifier)
	assert param_0_1.name == "y"

	param_0_2 = body_0.params[2]
	assert isinstance(param_0_2, Node.Identifier)
	assert param_0_2.name == "z"

	# {
	assert isinstance(body_0.body, Node.BlockStatement)
	assert len(body_0.body.body) == 2

	# super(x, y);
	e = body_0.body.body[0]
	assert isinstance(e, Node.ExpressionStatement)
	body_0_0 = e.expression
	assert isinstance(body_0_0, Node.CallExpression)
	assert isinstance(body_0_0.callee, Node.Super)
	assert len(body_0_0.arguments) == 2

	# x
	body_0_args_0 = body_0_0.arguments[0]
	assert isinstance(body_0_args_0, Node.Identifier)
	assert body_0_args_0.name == "x"

	# y
	body_0_args_1 = body_0_0.arguments[1]
	assert isinstance(body_0_args_1, Node.Identifier)
	assert body_0_args_1.name == "y"

	# this.z = z;
	e = body_0.body.body[1]
	assert isinstance(e, Node.ExpressionStatement)
	body_0_1 = e.expression
	assert isinstance(body_0_1, Node.ComplexExpression)
	assert body_0_1.type == "AssignmentExpression"
	assert body_0_1.operator == "="

	# this.z
	assert isinstance(body_0_1.left, Node.MemberExpression)
	assert body_0_1.left.computed is False
	assert isinstance(body_0_1.left.object, Node.ThisExpression)
	assert isinstance(body_0_1.left.property, Node.Identifier)
	assert body_0_1.left.property.name == "z"

	# = z;
	assert isinstance(body_0_1.right, Node.Identifier)
	assert body_0_1.right.name == "z"
	# }

	# def calc()
	body_1 = node.body.body[1]
	assert isinstance(body_1, Node.FunctionDeclaration)
	assert body_1.name.name == "calc"
	assert len(body_1.params) == 0

	# {
	assert isinstance(body_1.body, Node.BlockStatement)
	assert len(body_1.body.body) == 1

	# return super() + this.y;
	body_1_0 = body_1.body.body[0]
	assert isinstance(body_1_0, Node.ReturnStatement)
	assert isinstance(body_1_0.argument, Node.ComplexExpression)

	# super() + this.y;
	assert body_1_0.argument.type == "BinaryExpression"
	assert body_1_0.argument.operator == "+"

	# super()
	assert isinstance(body_1_0.argument.left, Node.CallExpression)
	assert isinstance(body_1_0.argument.left.callee, Node.Super)
	assert len(body_1_0.argument.left.arguments) == 0

	# this.z
	assert isinstance(body_1_0.argument.right, Node.MemberExpression)
	assert body_1_0.argument.right.computed is False

	# this
	assert isinstance(body_1_0.argument.right.object, Node.ThisExpression)

	# z
	assert isinstance(body_1_0.argument.right.property, Node.Identifier)
	assert body_1_0.argument.right.property.name == "z"


def testNewClassExpression():
	ast = Parser().parse("new Point3D(10, 20, 30);")

	assert len(ast.body) == 1

	node = ast.body[0]

	assert isinstance(node, Node.ExpressionStatement)

	expression = node.expression

	assert isinstance(expression, Node.NewExpression)
	assert isinstance(expression.callee, Node.Identifier)
	assert expression.callee.name == "Point3D"

	assert len(expression.arguments) == 3

	arg0, arg1, arg2, *_ = expression.arguments

	for (arg, value) in [(arg0, 10), (arg1, 20), (arg2, 30)]:
		assert isinstance(arg, Node.Literal)
		assert arg.type == "IntegerLiteral"
		assert arg.value == value
