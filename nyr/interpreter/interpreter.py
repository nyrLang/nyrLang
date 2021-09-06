import logging
import math
import sys
from collections.abc import Callable
from enum import Enum

from nyr.interpreter.stack import ActivationRecord
from nyr.interpreter.stack import ARType
from nyr.interpreter.stack import Stack
from nyr.parser import node

MAXITERATIONS = 2 ** 16
MAXRECURSIONDEPTH = 128


class Log(Enum):
	logVisit = 0b1 << 0
	logStack = 0b1 << 1
	logFinal = 0b1 << 2

	logAll = logVisit | logStack | logFinal


class NodeVisitor:
	def visit(self, node: node.Node):
		if node is None:
			return None
		vName = f"visit{type(node).__name__}"
		visitor: Callable = getattr(self, vName, self.genericVisit)
		return visitor(node)

	def genericVisit(self, node):  # pragma: no cover
		raise Exception(f"visit{type(node).__name__} not found")


class Interpreter(NodeVisitor):
	ast: node.Program
	stack: Stack
	fns: list = []
	logging: int

	def __init__(self, log: int = 0):
		self.logging = log

		hdlr = logging.StreamHandler(sys.stdout)
		hdlr.setFormatter(logging.Formatter("[ %(name)s ] | %(levelname)s | %(message)s"))
		self.logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")
		self.logger.setLevel(logging.DEBUG)
		self.logger.addHandler(hdlr)

		# FIXME: Hacky way to break loops
		self.breakLoop = False

	def _reset(self):
		self.stack = Stack()
		self.fns = []

	def logVisit(self, msg):  # pragma: no cover
		if (self.logging & Log.logVisit.value) == Log.logVisit.value:
			self.logger.info(msg)

	def logStack(self, msg):  # pragma: no cover
		if (self.logging & Log.logStack.value) == Log.logStack.value:
			self.logger.debug(msg)

	def logFinal(self):  # pragma: no cover
		if (self.logging & Log.logFinal.value) == Log.logFinal.value:
			self.logger.debug(str(self.stack))

	def interpret(self, ast: node.Program):
		self._reset()
		return self.visit(ast)

	def visitProgram(self, node: node.Program):
		self.logVisit("ENTER: Node.Program")

		ar = ActivationRecord(
			node.type,
			ARType.PROGRAM,
			1,
		)
		self.stack.push(ar)

		self.logStack(str(ar))

		for n in node.body:
			self.visit(n)

		self.logVisit("LEAVE: Node.Program")
		self.logStack(str(self.stack))
		self.logFinal()
		return self.stack.pop().members

	# STATEMENTS

	def visitExpressionStatement(self, node: node.ExpressionStatement):
		self.logVisit("ENTER: Node.ExpressionStatement")
		r = self.visit(node.expression)
		if r == "break":
			self.breakLoop = True
		self.logVisit("LEAVE: Node.ExpressionStatement")

	def visitEmptyStatement(self, _: node.EmptyStatement):
		pass

	def visitBlockStatement(self, node: node.BlockStatement):
		self.logVisit("ENTER: Node.BlockStatement")

		returns = []
		for n in node.body:
			r = self.visit(n)
			if r:
				returns.append(r)

		self.logVisit("LEAVE: Node.BlockStatement")

		if len(returns) == 0:  # pragma: no cover
			return
		elif len(returns) == 1:  # pragma: no cover
			return returns[0]
		else:  # pragma: no cover
			return returns

	def visitIfStatement(self, node: node.IfStatement):
		self.logVisit("ENTER: Node.IfStatement")
		test = self.visit(node.test)
		assert isinstance(test, bool), f"Expected bool, got {type(test).__name__} instead"
		if test is True:
			ret = self.visit(node.consequent)
		else:
			ret = self.visit(node.alternative)
		self.logVisit("LEAVE: Node.IfStatement")
		return ret

	def visitVariableStatement(self, node: node.VariableStatement):
		self.logVisit("ENTER: Node.VariableStatement")
		for decl in node.declarations:
			self.visit(decl)
		self.logVisit("LEAVE: Node.VariableStatement")

	def visitWhileStatement(self, node: node.WhileStatement):
		self.logVisit("ENTER: Node.WhileStatement")
		test = self.visit(node.test)
		assert isinstance(test, bool), f"Interpreter::Node.WhileStatement: Expected bool, got {type(test)} instead"

		iterations = 0
		while test is True:
			self.visit(node.body)
			test = self.visit(node.test)
			assert isinstance(test, bool), f"Interpreter::Node.WhileStatement: Expected bool, got {type(test)} instead"

			iterations += 1

			if iterations > MAXITERATIONS:
				raise Exception(f"Exceeded {MAXITERATIONS} iterations in while statement")

			# FIXME: hacky way to break loops
			if self.breakLoop is True:
				self.breakLoop = False
				break

		self.logVisit("LEAVE: Node.WhileStatement")

	def visitDoWhileStatement(self, node: node.DoWhileStatement):
		self.logVisit("ENTER: Node.DoWhileStatement")
		self.visit(node.body)
		test = self.visit(node.test)
		assert isinstance(test, bool), f"Interpreter::Node.DoWhileStatement: Expected bool, got {type(test)} instead"

		iterations = 0
		while test is True:
			self.visit(node.body)
			test = self.visit(node.test)
			assert isinstance(test, bool), f"Interpreter::Node.DoWhileStatement: Expected bool, got {type(test)} instead"

			iterations += 1

			if iterations > MAXITERATIONS:
				raise Exception(f"Exceeded {MAXITERATIONS} iterations in do-while statement")

			# FIXME: hacky way to break loops
			if self.breakLoop is True:
				self.breakLoop = False
				break

		self.logVisit("LEAVE: Node.DoWhileStatement")

	def visitForStatement(self, node: node.ForStatement):
		self.logVisit("ENTER: Node.ForStatement")
		tempDecls = []
		if node.init is not None:
			if isinstance(node.init, node.VariableStatement):
				for decl in node.init.declarations:
					tempDecls.append(decl.id.name)
			self.visit(node.init)
		test = True
		if node.test is not None:
			test = self.visit(node.test)
			assert isinstance(test, bool), f"Interpreter::Node.ForStatement: Expected bool, got {type(test)} instead"

		iterations = 0
		while test is True:
			self.visit(node.body)
			self.visit(node.update)

			if node.test is not None:
				test = self.visit(node.test)
				assert isinstance(test, bool), f"Interpreter::Node.ForStatement: Expected bool, got {type(test)} instead"
			iterations += 1

			if iterations > MAXITERATIONS:
				raise Exception(f"Exceeded {MAXITERATIONS} iterations in for statement")

			# FIXME: hacky way to break loops
			if self.breakLoop is True:
				self.breakLoop = False
				break

		for decl in tempDecls:
			del self.stack.peek().members[decl]
		del tempDecls

		self.logVisit("LEAVE: Node.ForStatement")

	def visitReturnStatement(self, node: node.ReturnStatement):
		self.logVisit("ENTER: Node.ReturnStatement")
		ret = self.visit(node.argument)
		self.logVisit("LEAVE: Node.ReturnStatement")
		return ret

	# EXPRESSIONS

	def visitComplexExpression(self, node: node.ComplexExpression):
		self.logVisit("ENTER: Node.ComplexExpression")

		if isinstance(node.left, node.Identifier):
			left = node.left.name
		else:
			left = self.visit(node.left)

		if isinstance(node.right, node.Identifier):
			right = node.right.name
		else:
			right = self.visit(node.right)

		if type(left) == str:
			if self.stack.peek().varExists(left):
				lVal = self.stack.peek().get(left)
			else:
				lVal = f'{left}'
		else:
			lVal = left

		if type(right) == str:
			if self.stack.peek().varExists(right):
				rVal = self.stack.peek().get(right)
			else:
				rVal = f'{right}'
		else:
			rVal = right

		if left is None:  # pragma: no cover
			raise Exception(f"Unknown left-hand side of ComplexExpression: {node.left}")
		if right is None:  # pragma: no cover
			raise Exception(f"Unknown right-hand side of ComplexExpression: {node.right}")

		_res = None
		if node.type == "BinaryExpression":
			if node.operator == "/":
				assert lVal is not None, f"Expected value, got None instead"
				assert rVal is not None, f"Expected value, got None instead"
				try:
					res = eval(f"{lVal} / {rVal}")
				except ZeroDivisionError:
					raise ZeroDivisionError(f"Cannot divide by 0")

				if math.floor(res) == math.ceil(res):
					_res = int(res)
				else:
					_res = float(res)
			else:
				assert lVal is not None, f"Expected value, got None instead"
				assert rVal is not None, f"Expected value, got None instead"
				if type(lVal) == str: lVal = f'"{lVal}"'
				if type(rVal) == str: rVal = f'"{rVal}"'
				_res = eval(f"{lVal} {node.operator} {rVal}")
		elif node.type == "AssignmentExpression":
			ar = self.stack.peek()
			if not ar.varExists(left):
				raise Exception(f'Variable "{left}" does not exist in available scope')

			if node.operator != "=":
				op = node.operator[0]
				assert lVal is not None, f"Expected value, got None instead"
				assert rVal is not None, f"Expected value, got None instead"
				if type(lVal) == str: lVal = f'"{lVal}"'
				if type(rVal) == str: rVal = f'"{rVal}"'
				rVal = eval(f"{lVal} {op} {rVal}")

			ar[left] = rVal
		elif node.type == "LogicalExpression":
			if node.operator == "&&":
				operator = "and"
			elif node.operator == "||":
				operator = "or"
			else:  # pragma: no cover
				# **should** not happen
				raise Exception(f"Unknown operator in Logical Expression: {node.operator}")
			_res = eval(f"{lVal} {operator} {rVal}")
		elif node.type == "BitwiseExpression":
			assert lVal is not None, f"Expected value, got None instead"
			assert rVal is not None, f"Expected value, got None instead"
			_res = eval(f"{lVal} {node.operator} {rVal}")
		else:  # pragma: no cover
			raise Exception(f"Unknown ComplexExpression: {node}")
		self.logVisit("LEAVE: Node.ComplexExpression")
		return _res

	def visitUnaryExpression(self, node: node.UnaryExpression):
		self.logVisit("ENTER: Node.UnaryExpression")
		val = self.visit(node.argument)
		if val is None:
			raise Exception(f'Cannot use {node.operator} on "null"')
		else:
			if node.operator == "!":
				val = eval(f"not {val}", self.stack.peek().members)
			else:
				val = eval(f"{node.operator}{val}", self.stack.peek().members)
		self.logVisit("LEAVE: Node.UnaryExpression")
		return val

	def visitCallExpression(self, node: node.CallExpression):
		if node.callee.name not in self.fns:
			raise Exception(f'Function "{node.callee.name}" does not exist in available scope')
		if node.fn is None:  # pragma: no cover
			raise Exception(f'Failed to aquire function for "{node.callee.name}"')
		assert len(node.arguments) == len(node.fn.get("args")), f"Incorrect amount of arguments given. Expected {len(node.fn.get('args'))}, got {len(node.arguments)}"

		ar = ActivationRecord(
			node.type,
			ARType.FUNCTION,
			self.stack.peek().nestingLevel + 1,
		)
		if ar.nestingLevel > MAXRECURSIONDEPTH:
			raise Exception(f'Exceeded recursion depth of {MAXRECURSIONDEPTH} in function "{node.callee.name}"')
		for argName, argValue in zip(node.fn.get("args", {}), node.arguments):
			if isinstance(argName, node.Identifier):
				ar[argName.name] = self.visit(argValue)
			else:
				ar[argName] = self.visit(argValue)

		self.stack.push(ar)
		self.logVisit(f"ENTER: Node.CallExpression({node.callee.name}, {ar.members})")
		self.logStack(str(self.stack))

		f = node.fn.get("body", None)
		assert f is not None, f'Failed to aquire function body for "{node.callee.name}"'

		ret = self.visit(f)

		self.logVisit(f"LEAVE: Node.CallExpression({node.callee.name})")
		self.logStack(str(self.stack))
		self.stack.pop()
		return ret

	# def visitSuperExpression(self, node: Node.SuperExpression):
	# 	self.lVisit("ENTER: Node.SuperExpression")
	# 	self.lVisit("LEAVE: Node.SuperExpression")

	# def visitThisExpression(self, node: Node.ThisExpression):
	# 	self.lVisit("ENTER: Node.ThisExpression")
	# 	self.lVisit("LEAVE: Node.ThisExpression")

	# def visitNewExpression(self, node: Node.NewExpression):
	# 	self.lVisit("ENTER: Node.NewExpression")
	# 	self.lVisit("LEAVE: Node.NewExpression")

	# DECLARATIONS

	def visitVariableDeclaration(self, node: node.VariableDeclaration):
		varName = self.visit(node.id)
		varValue = self.visit(node.init)
		_vv = f'"{varValue}"' if type(varValue) == str else varValue
		self.logVisit(f"ENTER: Node.VariableDeclaration({varName}, {_vv})")
		ar = self.stack.peek()
		if ar.varExists(varName):
			# FIXME: Does not happen for some reason
			raise Exception(f'Variable "{varName}" already exists in available scope')
		elif type(varName) != str:
			raise Exception(f'Unknown variable "{varName}"')
		ar[varName] = varValue
		self.logVisit(f"LEAVE: Node.VariableDeclaration({varName}, {_vv})")
		del _vv

	def visitFunctionDeclaration(self, node: node.FunctionDeclaration):
		self.logVisit(f"ENTER: Node.FunctionDeclaration({node.name.name})")
		if node.name.name in self.fns:
			raise Exception(f'Function "{node.name.name}" already exists in available scope')
		self.fns.append(node.name.name)
		self.logVisit(f"LEAVE: Node.FunctionDeclaration({node.name.name})")

	# def visitClassDeclaration(self, node: Node.ClassDeclaration):
	# 	self.lVisit("ENTER: Node.ClassDeclaration")
	# 	self.lVisit("LEAVE: Node.ClassDeclaration")

	# OTHER

	def visitIdentifier(self, node: node.Identifier):
		self.logVisit("ENTER: Node.Identifier")
		if self.stack.peek().varExists(node.name):
			val = self.stack.peek().members.get(node.name)
		else:
			val = node.name
		self.logVisit("LEAVE: Node.Identifier")
		return val

	def visitLiteral(self, node: node.Literal):
		self.logVisit("ENTER: Node.Literal")
		self.logVisit("LEAVE: Node.Literal")
		return node.value
