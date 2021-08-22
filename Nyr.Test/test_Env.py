import pytest

from Nyr.Interpreter.Env import Env
from Nyr.Parser import Node


@pytest.mark.dependency()
def testAddValue():
	env = Env()
	env.addValue("varName", 17)
	env.addValue("anotherVarName", "varName")

	with pytest.raises(Exception, match="Variable varName already exists"):
		env.addValue("varName", 42)

	assert env == {"varName": 17, "anotherVarName": 17}


@pytest.mark.dependency(depends=["testAddValue"])
def testGetValue():
	env = Env()
	env.addValue("x", "A String")

	assert env.getValue("x") == "A String"
	assert env.getValue(-5) == -5

	with pytest.raises(Exception, match="Variable with name z does not exist in available scope"):
		env.setValue("z", 666)

	assert env == {"x": "A String"}


@pytest.mark.dependency(depends=["testAddValue"])
def testSetValue():
	env = Env()
	env.addValue("x", "A String")
	env.addValue("y", None)

	env.setValue("y", "x")
	env.setValue("x", 3.14159)

	with pytest.raises(Exception, match="Variable with name z does not exist in available scope"):
		env.setValue("z", 666)

	assert env == {"x": 3.14159, "y": "A String"}


@pytest.mark.dependency(depends=["testAddValue", "testGetValue", "testSetValue"])
def testFindOwner():
	env1 = Env()
	env2 = Env(parent=env1)

	env1.addValue("x", 2.178)

	assert env1.findOwner("x") == env1
	assert env1.findOwner("y") is None

	assert env2.findOwner("x") == env1
	assert env2.findOwner("y") is None

	assert env2.getValue("x") == 2.178

	env2.setValue("x", 55)

	assert env1 == {"x": 55}
	assert env2 == {}


@pytest.mark.dependency()
def testAddFunc():
	env = Env()
	env.addFunc(
		"foo", {
			"args": ["arg1", "arg2"],
			"body": Node.FunctionDeclaration(
				"foo",
				[Node.Identifier("arg1"), Node.Identifier("arg2")],
				Node.BlockStatement([
					Node.ReturnStatement(
					Node.ComplexExpression(
						"BinaryExpression",
						"+",
						Node.Identifier("arg1"),
						Node.Identifier("arg2"),
					),
					),
				]),
			),
		},
	)

	with pytest.raises(Exception, match='Function "foo" already defined'):
		# No need to add dict since it will raise an exception
		env.addFunc("foo", {})



@pytest.mark.dependency(depends=["testAddFunc"])
def testGetFunc():
	env = Env()
	func = {
		"args": ["arg1", "arg2"],
		"body": Node.FunctionDeclaration(
			"foo",
			[Node.Identifier("arg1"), Node.Identifier("arg2")],
			Node.BlockStatement([
				Node.ReturnStatement(
					Node.ComplexExpression(
						"BinaryExpression",
						"+",
						Node.Identifier("arg1"),
						Node.Identifier("arg2"),
					),
				),
			]),
		),
	}
	env.addFunc("foo", func)

	assert env.getFunc("foo") == func

	with pytest.raises(Exception, match='Function with name "bar" does not exist in available scope'):
		env.getFunc("bar")


@pytest.mark.dependency(depends=["testAddFunc"])
def testFindFuncOwner():
	env1 = Env()
	env2 = Env(parent=env1)

	env1.addFunc(
		"foo", {
			"args": ["arg1", "arg2"],
			"body": Node.FunctionDeclaration(
				"foo",
				[Node.Identifier("arg1"), Node.Identifier("arg2")],
				Node.BlockStatement([
					Node.ReturnStatement(
						Node.ComplexExpression(
							"BinaryExpression",
							"+",
							Node.Identifier("arg1"),
							Node.Identifier("arg2"),
						),
					),
				]),
			),
		},
	)

	assert env1.findFuncOwner("foo") == env1
	assert env1.findFuncOwner("bar") is None

	assert env2.findFuncOwner("foo") == env1
	assert env2.findFuncOwner("bar") is None
