import json
from abc import abstractmethod
from typing import Any
from typing import Optional
from typing import Union


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

	@abstractmethod
	def toJSON(self): pass


class Program(Node):
	def __init__(self, body: list[Node]):
		self.type = self.__class__.__name__
		self.body = body

	def toJSON(self):
		return dict(type=self.type, body=self.body)


class VariableDeclaration(Node):
	def __init__(self, id_: Node, init: Optional[Node]):
		self.type = self.__class__.__name__
		self.id = id_
		self.init = init

	def toJSON(self):
		return dict(type=self.type, id=self.id, init=self.init)


class Identifier(Node):
	def __init__(self, name: str):
		self.type = self.__class__.__name__
		self.name = name

	def toJSON(self):
		return dict(type=self.type, name=self.name)


# Statements
class ExpressionStatement(Node):
	def __init__(self, expression: Node):
		self.type = self.__class__.__name__
		self.expression = expression

	def toJSON(self):
		return dict(type=self.type, expression=self.expression)


class EmptyStatement(Node):
	def __init__(self):
		self.type = self.__class__.__name__

	def toJSON(self):
		return dict(type=self.type)


class BlockStatement(Node):
	def __init__(self, body: list[Node]):
		self.type = self.__class__.__name__
		self.body = body

	def toJSON(self):
		return dict(type=self.type, body=self.body)


class IfStatement(Node):
	def __init__(self, test: Node, consequent: Node, alternative: Optional[Node]):
		self.type = self.__class__.__name__
		self.test = test
		self.consequent = consequent
		self.alternative = alternative

	def toJSON(self):
		return dict(type=self.type, test=self.test, consequent=self.consequent, alternative=self.alternative)


class VariableStatement(Node):
	def __init__(self, declarations: list[Node]):
		self.type = self.__class__.__name__
		self.declarations = declarations

	def toJSON(self):
		return dict(type=self.type, declarations=self.declarations)


class WhileStatement(Node):
	def __init__(self, type_: str, test: Node, body: Node):
		self.type = type_
		self.test = test
		self.body = body

	def toJSON(self):
		if self.type == "WhileStatement":
			return dict(type=self.type, test=self.test, body=self.body)
		elif self.type == "DoWhileStatement":
			return dict(type=self.type, body=self.body, test=self.test)
		else: raise Exception(f"Unknown While loop: {self.type}")


class ForStatement(Node):
	def __init__(self, init: Optional[Node], test: Optional[Node], update: Optional[Node], body: Node):
		self.type = self.__class__.__name__
		self.init = init
		self.test = test
		self.update = update
		self.body = body

	def toJSON(self):
		return dict(type=self.type, init=self.init, test=self.test, update=self.update, body=self.body)


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


class UnaryExpression(Node):
	def __init__(self, operator: str, argument: Node):
		self.type = self.__class__.__name__
		self.operator = operator
		self.argument = argument

	def toJSON(self):
		return dict(type=self.type, operator=self.operator, argument=self.argument)


class MemberExpression(Node):
	computed: bool
	object: Node
	property: Node

	def __init__(self, computed: bool, object_: Node, property_: Node):
		self.type = "MemberExpression"
		self.computed = computed
		self.object = object_
		self.property = property_

	def toJSON(self):
		return dict(type=self.type, computed=self.computed, object=self.object, property=self.property)


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


class ReturnStatement(Node):
	def __init__(self, argument: Optional[Node]):
		self.type = self.__class__.__name__
		self.argument = argument

	def toJSON(self):
		return dict(type=self.type, argument=self.argument)


class CallExpression(Node):
	callee: Node
	arguments: list[Node]

	def __init__(self, callee: Node, arguments: list[Node]):
		self.type = self.__class__.__name__
		self.callee = callee
		self.arguments = arguments

	def toJSON(self):
		return dict(type=self.type, callee=self.callee, arguments=self.arguments)


# Literals
class Literal(Node):
	value: NodeValue

	def __init__(self, type_: str, value: NodeValue):
		self.type = type_
		self.value = value

	def toJSON(self):
		return dict(type=self.type, value=self.value)
