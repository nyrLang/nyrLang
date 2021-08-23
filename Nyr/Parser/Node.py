from __future__ import annotations

import json
from typing import Any
from typing import Optional
from typing import Union


class ComplexEncoder(json.JSONEncoder):  # pragma: no cover
	def default(self, o: Any) -> Any:
		if hasattr(o, "toJSON"):
			return o.toJSON()
		else:
			return json.JSONEncoder.default(self, o)


NodeValue = Union[None, int, float, bool, str]


class Node:
	type: str
	value: NodeValue = None

	def __init__(self, type_: str):
		self.type = type_

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}('{self.type}')"

	def toJSON(self):  # pragma: no cover
		raise NotImplementedError(f"{self.__class__.__name__}.toJSON() has not been implemented")


class Program(Node):
	def __init__(self, body: list[Node]):
		super().__init__(self.__class__.__name__)
		self.body = body

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.body!r})"

	def toJSON(self):
		return dict(type=self.type, body=self.body)


class VariableDeclaration(Node):
	def __init__(self, id_: Identifier, init: Union[None, Identifier, Literal]):
		super().__init__(self.__class__.__name__)
		self.id = id_
		self.init = init

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.id!r}, {self.init!r})"

	def toJSON(self):
		return dict(type=self.type, id=self.id, init=self.init)


class Identifier(Node):
	def __init__(self, name: str):
		super().__init__(self.__class__.__name__)
		self.name = name

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}('{self.name}')"

	def toJSON(self):
		return dict(type=self.type, name=self.name)


# Statements
class ExpressionStatement(Node):
	def __init__(self, expression: Node):
		super().__init__(self.__class__.__name__)
		self.expression = expression

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.expression!r})"

	def toJSON(self):
		return dict(type=self.type, expression=self.expression)


class EmptyStatement(Node):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def toJSON(self):
		return dict(type=self.type)


class BlockStatement(Node):
	def __init__(self, body: list[Node]):
		super().__init__(self.__class__.__name__)
		self.body = body

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.body!r})"

	def toJSON(self):
		return dict(type=self.type, body=self.body)


class IfStatement(Node):
	def __init__(self, test: Node, consequent: Node, alternative: Optional[Node]):
		super().__init__(self.__class__.__name__)
		self.test = test
		self.consequent = consequent
		self.alternative = alternative

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.test!r}, {self.consequent!r}, {self.alternative!r})"

	def toJSON(self):
		return dict(type=self.type, test=self.test, consequent=self.consequent, alternative=self.alternative)


class VariableStatement(Node):
	def __init__(self, declarations: list[Node]):
		super().__init__(self.__class__.__name__)
		self.declarations = declarations

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.declarations!r})"

	def toJSON(self):
		return dict(type=self.type, declarations=self.declarations)


class WhileStatement(Node):
	def __init__(self, test: Node, body: Node):
		super().__init__(self.__class__.__name__)
		self.test = test
		self.body = body

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.test!r}, {self.body!r})"

	def toJSON(self):
		return dict(type=self.type, test=self.test, body=self.body)


class DoWhileStatement(Node):
	def __init__(self, body: Node, test: Node):
		super().__init__(self.__class__.__name__)
		self.test = test
		self.body = body

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.body!r}, {self.test!r})"

	def toJSON(self):
		return dict(type=self.type, body=self.body, test=self.test)


class ForStatement(Node):
	def __init__(self, init: Optional[Node], test: Optional[Node], update: Optional[Node], body: Node):
		super().__init__(self.__class__.__name__)
		self.init = init
		self.test = test
		self.update = update
		self.body = body

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.init!r}, {self.test!r}, {self.update!r}, {self.body!r})"

	def toJSON(self):
		return dict(type=self.type, init=self.init, test=self.test, update=self.update, body=self.body)


# Expressions
class ComplexExpression(Node):
	type: str
	operator: str
	left: Node
	right: Node

	def __init__(self, type_: str, operator: str, left: Node, right: Node):
		super().__init__(type_)
		self.operator = operator
		self.left = left
		self.right = right

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.type}, {self.operator}, {self.left!r}, {self.right!r})"

	def toJSON(self):
		return dict(type=self.type, operator=self.operator, left=self.left, right=self.right)


class UnaryExpression(Node):
	def __init__(self, operator: str, argument: Node):
		super().__init__(self.__class__.__name__)
		self.operator = operator
		self.argument = argument

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.operator}, {self.argument!r})"

	def toJSON(self):
		return dict(type=self.type, operator=self.operator, argument=self.argument)


class MemberExpression(Node):
	computed: bool
	object: Node
	property: Node

	def __init__(self, computed: bool, object_: Node, property_: Node):
		super().__init__(self.__class__.__name__)
		self.computed = computed
		self.object = object_
		self.property = property_

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.computed}, {self.object!r}, {self.property!r})"

	def toJSON(self):
		return dict(type=self.type, computed=self.computed, object=self.object, property=self.property)


# Functions
class FunctionDeclaration(Node):
	name: Identifier
	params: list[Node]
	body: Node

	def __init__(self, name: Identifier, parameters: list[Node], body: Node):
		super().__init__(self.__class__.__name__)
		self.name = name
		self.params = parameters
		self.body = body

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.name!r}, {self.params!r}, {self.body!r})"

	def toJSON(self):
		return dict(type=self.type, name=self.name, params=self.params, body=self.body)


class ReturnStatement(Node):
	def __init__(self, argument: Optional[Node]):
		super().__init__(self.__class__.__name__)
		self.argument = argument

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.argument!r})"

	def toJSON(self):
		return dict(type=self.type, argument=self.argument)


class CallExpression(Node):
	callee: Identifier
	arguments: list[Node]

	def __init__(self, callee: Identifier, arguments: list[Node]):
		super().__init__(self.__class__.__name__)
		self.callee = callee
		self.arguments = arguments

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.callee!r}, {self.arguments!r})"

	def toJSON(self):
		return dict(type=self.type, callee=self.callee, arguments=self.arguments)


# Classes
class ClassDeclaration(Node):
	id: Node
	superClass: Optional[Node]
	body: Node

	def __init__(self, id_: Node, superClass: Optional[Node], body: Node):
		super().__init__(self.__class__.__name__)
		self.id = id_
		self.superClass = superClass
		self.body = body

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.id!r}, {self.superClass!r}, {self.body!r})"

	def toJSON(self):
		return dict(type=self.type, id=self.id, superClass=self.superClass, body=self.body)


class Super(Node):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def toJSON(self):
		return dict(type=self.type)


class ThisExpression(Node):
	def __init__(self):
		super().__init__(self.__class__.__name__)

	def toJSON(self):
		return dict(type=self.type)


class NewExpression(Node):
	callee: Node
	arguments: list[Node]

	def __init__(self, callee: Node, arguments: list[Node]):
		super().__init__(self.__class__.__name__)
		self.callee = callee
		self.arguments = arguments

	def __repr__(self):  # pragma: no cover
		return f"{self.__module__}.{self.__class__.__name__}({self.callee!r}, {self.arguments!r})"

	def toJSON(self):
		return dict(type=self.type, callee=self.callee, arguments=self.arguments)


# Literals
class Literal(Node):
	value: NodeValue

	def __init__(self, type_: str, value: NodeValue):
		super().__init__(type_)
		self.value = value

	def __repr__(self):  # pragma: no cover
			return f"{self.__module__}.{self.__class__.__name__}({self.type}, {self.value})"

	def toJSON(self):
		return dict(type=self.type, value=self.value)
