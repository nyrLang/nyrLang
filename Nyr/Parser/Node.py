import json
from abc import abstractmethod
from typing import Any
from typing import Optional


class ComplexEncoder(json.JSONEncoder):
	def default(self, o: Any) -> Any:
		if hasattr(o, "toJSON"):
			return o.toJSON()
		else:
			return json.JSONEncoder.default(self, o)


class Node:
	type: str
	value: Any

	@abstractmethod
	def toJSON(self): pass


class Program(Node):
	def __init__(self, body: list[Node]):
		self.type = self.__class__.__name__
		self.body = body

	def toJSON(self):
		return dict(type=self.type, body=self.body)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class IfStatement(Node):
	def __init__(self, test: Node, consequent: Node, alternative: Optional[Node]):
		self.type = self.__class__.__name__
		self.test = test
		self.consequent = consequent
		self.alternative = alternative

	def toJSON(self):
		return dict(type=self.type, test=self.test, consequent=self.consequent, alternative=self.alternative)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class VariableStatement(Node):
	def __init__(self, declarations: list[Node]):
		self.type = self.__class__.__name__
		self.declarations = declarations

	def toJSON(self):
		return dict(type=self.type, declarations=self.declarations)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class VariableDeclaration(Node):
	def __init__(self, id_: Node, init: Optional[Node]):
		self.type = self.__class__.__name__
		self.id = id_
		self.init = init

	def toJSON(self):
		return dict(type=self.type, id=self.id, init=self.init)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class EmptyStatement(Node):
	def __init__(self):
		self.type = self.__class__.__name__

	def toJSON(self):
		return dict(type=self.type)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class BlockStatement(Node):
	def __init__(self, body: list[Node]):
		self.type = self.__class__.__name__
		self.body = body

	def toJSON(self):
		return dict(type=self.type, body=self.body)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class ExpressionStatement(Node):
	def __init__(self, expression: Node):
		self.type = self.__class__.__name__
		self.expression = expression

	def toJSON(self):
		return dict(type=self.type, expression=self.expression)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class AssignmentExpression(Node):
	def __init__(self, operator: str, left: Node, right: Node):
		self.type = self.__class__.__name__
		self.operator = operator
		self.left = left
		self.right = right

	def toJSON(self):
		return dict(type=self.type, operator=self.operator, left=self.left, right=self.right)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class Identifier(Node):
	def __init__(self, name: str):
		self.type = self.__class__.__name__
		self.name = name

	def toJSON(self):
		return dict(type=self.type, name=self.name)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class BinaryExpression(Node):
	def __init__(self, operator: str, left: Node, right: Node):
		self.type = self.__class__.__name__
		self.operator = operator
		self.left = left
		self.right = right

	def toJSON(self):
		return dict(type=self.type, operator=self.operator, left=self.left, right=self.right)

	def value(self):
		raise ValueError(f"{self.__class__.__name__}.value should not be accessed")


class NullLiteral(Node):
	value: None

	def __init__(self):
		self.type = self.__class__.__name__
		self.value = None

	def toJSON(self):
		return dict(type=self.type, value=self.value)


class BooleanLiteral(Node):
	value: bool

	def __init__(self, value: bool):
		self.type = self.__class__.__name__
		self.value = value

	def toJSON(self):
		return dict(type=self.type, value=self.value)


class NumericLiteral(Node):
	value: int

	def __init__(self, value: int):
		self.type = self.__class__.__name__
		self.value = int(value)

	def toJSON(self):
		return dict(type=self.type, value=self.value)


class StringLiteral(Node):
	value: str

	def __init__(self, value: str):
		self.value = value
		self.type = self.__class__.__name__

	def toJSON(self):
		return dict(type=self.type, value=self.value)
