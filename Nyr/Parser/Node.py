import json
from abc import abstractmethod
from typing import Any
from typing import Optional
from typing import Union

from Nyr.Interpreter.Env import Env


class ComplexEncoder(json.JSONEncoder):
	def default(self, o: Any) -> Any:
		if hasattr(o, "toJSON"):
			return o.toJSON()
		else:
			return json.JSONEncoder.default(self, o)


NodeValue = Union[None, int, float, bool, str]


class Node:
	type: str
	value: NodeValue = None

	def toJSON(self):
		raise NotImplementedError(f"{self.__class__.__name__}.toJSON() has not been implemented")

	def toSExpression(self):
		raise NotImplementedError(f"{self.__class__.__name__}.toSExpression() has not been implemented")

	def exec(self, env: Env):
		raise NotImplementedError(f"{self.__class__.__name__}.exec() has not been implemented")


class Program(Node):
	def __init__(self, body: list[Node]):
		self.type = self.__class__.__name__
		self.body = body

	def toJSON(self):
		return dict(type=self.type, body=self.body)

	def toSExpression(self):
		body = []
		for b in self.body:
			body.append(b.toSExpression())
		return ["begin", body]


class VariableDeclaration(Node):
	def __init__(self, id_: Node, init: Optional[Node]):
		self.type = self.__class__.__name__
		self.id = id_
		self.init = init

	def toJSON(self):
		return dict(type=self.type, id=self.id, init=self.init)

	def toSExpression(self):
		init = self.init.toSExpression() if self.init else None
		return ["let", self.id.toSExpression(), init]


class Identifier(Node):
	def __init__(self, name: str):
		self.type = self.__class__.__name__
		self.name = name

	def toJSON(self):
		return dict(type=self.type, name=self.name)

	def toSExpression(self):
		return self.name

	def exec(self, env: Env):
		return self.name


# Statements
class ExpressionStatement(Node):
	def __init__(self, expression: Node):
		self.type = self.__class__.__name__
		self.expression = expression

	def toJSON(self):
		return dict(type=self.type, expression=self.expression)

	def toSExpression(self):
		return self.expression.toSExpression()


class EmptyStatement(Node):
	def __init__(self):
		self.type = self.__class__.__name__

	def toJSON(self):
		return dict(type=self.type)

	def toSExpression(self):
		return


class BlockStatement(Node):
	def __init__(self, body: list[Node]):
		self.type = self.__class__.__name__
		self.body = body

	def toJSON(self):
		return dict(type=self.type, body=self.body)

	def toSExpression(self):
		body = []
		for b in self.body:
			body.append(b.toSExpression())
		return body


class IfStatement(Node):
	def __init__(self, test: Node, consequent: Node, alternative: Optional[Node]):
		self.type = self.__class__.__name__
		self.test = test
		self.consequent = consequent
		self.alternative = alternative

	def toJSON(self):
		return dict(type=self.type, test=self.test, consequent=self.consequent, alternative=self.alternative)

	def toSExpression(self):
		alternative = self.alternative.toSExpression() if self.alternative else None
		return ["if", self.test.toSExpression(), alternative]


class VariableStatement(Node):
	def __init__(self, declarations: list[Node]):
		self.type = self.__class__.__name__
		self.declarations = declarations

	def toJSON(self):
		return dict(type=self.type, declarations=self.declarations)

	def toSExpression(self):
		vrs = []
		for var in self.declarations:
			vrs.append(var.toSExpression())
		return vrs


class WhileStatement(Node):
	def __init__(self, type_: str, test: Node, body: Node):
		self.type = type_
		self.test = test
		self.body = body

	def toJSON(self):
		return dict(type=self.type, test=self.test, body=self.body)

	def toSExpression(self):
		return ["while", self.test.toSExpression(), self.body.toSExpression()]


class DoWhileStatement(Node):
	def __init__(self, type_: str, test: Node, body: Node):
		self.type = type_
		self.test = test
		self.body = body

	def toJSON(self):
		return dict(type=self.type, body=self.body, test=self.test)

	def toSExpression(self):
		return ["while", self.test.toSExpression(), self.body.toSExpression()]


class ForStatement(Node):
	def __init__(self, init: Optional[Node], test: Optional[Node], update: Optional[Node], body: Node):
		self.type = self.__class__.__name__
		self.init = init
		self.test = test
		self.update = update
		self.body = body

	def toJSON(self):
		return dict(type=self.type, init=self.init, test=self.test, update=self.update, body=self.body)

	def toSExpression(self):
		init = self.init.toSExpression() if self.init else None
		test = self.test.toSExpression() if self.test else None
		update = self.update.toSExpression() if self.update else None
		return ["for", init, test, update, self.body.toSExpression()]


# Expressions
class ComplexExpression(Node):
	type: str
	operator: str
	left: Node
	right: Node

	def __init__(self, type_: str, operator: str, left: Node, right: Node):
		self.type = type_
		self.operator = operator
		self.left = left
		self.right = right

	def toJSON(self):
		return dict(type=self.type, operator=self.operator, left=self.left, right=self.right)

	def toSExpression(self):
		return [self.operator, self.left.toSExpression(), self.right.toSExpression()]


class UnaryExpression(Node):
	def __init__(self, operator: str, argument: Node):
		self.type = self.__class__.__name__
		self.operator = operator
		self.argument = argument

	def toJSON(self):
		return dict(type=self.type, operator=self.operator, argument=self.argument)

	def toSExpression(self):
		if self.argument.type == "IntegerLiteral":
			return int(f"{self.operator}{self.argument.toSExpression()}")
		elif self.argument.type == "FloatLiteral":
			return float(f"{self.operator}{self.argument.toSExpression()}")
		else:
			raise Exception(f"Unknown right hand side of UnaryExpression: {self.argument.type}")


class MemberExpression(Node):
	computed: bool
	object: Node
	property: Node

	def __init__(self, computed: bool, object_: Node, property_: Node):
		self.type = self.__class__.__name__
		self.computed = computed
		self.object = object_
		self.property = property_

	def toJSON(self):
		return dict(type=self.type, computed=self.computed, object=self.object, property=self.property)

	def toSExpression(self):
		return [".", self.object.toSExpression(), self.property.toSExpression(), self.computed]


# Functions
class FunctionDeclaration(Node):
	name: Identifier
	params: list[Node]
	body: Node

	def __init__(self, name: Identifier, parameters: list[Node], body: Node):
		self.type = self.__class__.__name__
		self.name = name
		self.params = parameters
		self.body = body

	def toJSON(self):
		return dict(type=self.type, name=self.name, params=self.params, body=self.body)

	def toSExpression(self):
		params = []
		for param in self.params:
			params.append(param.toSExpression())
		return ["def", params, self.body.toSExpression()]


class ReturnStatement(Node):
	def __init__(self, argument: Optional[Node]):
		self.type = self.__class__.__name__
		self.argument = argument

	def toJSON(self):
		return dict(type=self.type, argument=self.argument)

	def toSExpression(self):
		arg = self.argument.toSExpression() if self.argument else None
		return ["return", arg]


class CallExpression(Node):
	callee: Node
	arguments: list[Node]

	def __init__(self, callee: Node, arguments: list[Node]):
		self.type = self.__class__.__name__
		self.callee = callee
		self.arguments = arguments

	def toJSON(self):
		return dict(type=self.type, callee=self.callee, arguments=self.arguments)

	def toSExpression(self):
		args = []
		for arg in self.arguments:
			args.append(arg.toSExpression())
		return ["call", self.callee.toSExpression(), args]


# Classes
class ClassDeclaration(Node):
	id: Node
	superClass: Optional[Node]
	body: Node

	def __init__(self, id_: Node, superClass: Optional[Node], body: Node):
		self.type = self.__class__.__name__
		self.id = id_
		self.superClass = superClass
		self.body = body

	def toJSON(self):
		return dict(type=self.type, id=self.id, superClass=self.superClass, body=self.body)

	def toSExpression(self):
		superClass = self.superClass.toSExpression() if self.superClass else None
		return ["class", self.id.toSExpression(), superClass, self.body.toSExpression()]


class Super(Node):
	def __init__(self):
		self.type = self.__class__.__name__

	def toJSON(self):
		return dict(type=self.type)

	def toSExpression(self):
		return "super"


class ThisExpression(Node):
	def __init__(self):
		self.type = self.__class__.__name__

	def toJSON(self):
		return dict(type=self.type)

	def toSExpression(self):
		return "this"


class NewExpression(Node):
	callee: Node
	arguments: list[Node]

	def __init__(self, callee: Node, arguments: list[Node]):
		self.type = self.__class__.__name__
		self.callee = callee
		self.arguments = arguments

	def toJSON(self):
		return dict(type=self.type, callee=self.callee, arguments=self.arguments)

	def toSExpression(self):
		args = []
		for arg in self.arguments:
			args.append(arg.toSExpression())
		return ["new", self.callee.toSExpression(), args]


# Literals
class Literal(Node):
	value: NodeValue

	def __init__(self, type_: str, value: NodeValue):
		self.type = type_
		self.value = value

	def toJSON(self):
		return dict(type=self.type, value=self.value)

	def toSExpression(self):
		return self.value

	def exec(self, env: Env):
		return self.value
