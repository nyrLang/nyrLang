import Nyr.Parser.Node as Node
from Nyr.Parser.Parser import Parser


def testDeclarationWithAssign():
	ast = Parser().parse("let x = 42;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.VariableStatement)
	assert len(node.declarations) == 1

	declaration = node.declarations[0]
	assert isinstance(declaration, Node.VariableDeclaration)

	assert isinstance(declaration.id, Node.Identifier)
	assert declaration.id.name == "x"

	assert isinstance(declaration.init, Node.IntegerLiteral)
	assert declaration.init.value == 42


def testDeclarationWithoutAssign():
	ast = Parser().parse("let x;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.VariableStatement)
	assert len(node.declarations) == 1

	declaration = node.declarations[0]
	assert isinstance(declaration, Node.VariableDeclaration)

	assert isinstance(declaration.id, Node.Identifier)
	assert declaration.id.name == "x"

	assert declaration.init is None


def testMultipleDeclarationsWithoutAssign():
	ast = Parser().parse("let x, y;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.VariableStatement)
	assert len(node.declarations) == 2

	declaration1 = node.declarations[0]
	declaration2 = node.declarations[1]
	assert isinstance(declaration1, Node.VariableDeclaration)

	assert isinstance(declaration1.id, Node.Identifier)
	assert declaration1.id.name == "x"

	assert declaration1.init is None

	assert isinstance(declaration2, Node.VariableDeclaration)

	assert isinstance(declaration2.id, Node.Identifier)
	assert declaration2.id.name == "y"

	assert declaration2.init is None


def testMultipleDeclarationsWithPartialAssign():
	ast = Parser().parse("let x, y = 42;")

	assert len(ast.body) == 1

	node = ast.body[0]
	assert isinstance(node, Node.VariableStatement)
	assert len(node.declarations) == 2

	declaration1 = node.declarations[0]
	declaration2 = node.declarations[1]
	assert isinstance(declaration1, Node.VariableDeclaration)

	assert isinstance(declaration1.id, Node.Identifier)
	assert declaration1.id.name == "x"

	assert declaration1.init is None

	assert isinstance(declaration2, Node.VariableDeclaration)

	assert isinstance(declaration2.id, Node.Identifier)
	assert declaration2.id.name == "y"

	assert isinstance(declaration2.init, Node.IntegerLiteral)
	assert declaration2.init.value == 42
