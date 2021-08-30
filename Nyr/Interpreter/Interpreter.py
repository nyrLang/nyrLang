import logging
import math
import sys
from collections.abc import Callable

from Nyr.Interpreter.Stack import ActivationRecord
from Nyr.Interpreter.Stack import ARType
from Nyr.Interpreter.Stack import Stack
from Nyr.Parser import Node

MAXITERATIONS = 2 ** 16
MAXRECURSIONDEPTH = 128


class NodeVisitor:
	def visit(self, node: Node.Node):
		if node is None:
			return None
		vName = f"visit{type(node).__name__}"
		visitor: Callable = getattr(self, vName, self.genericVisit)
		return visitor(node)

	def genericVisit(self, node):  # pragma: no cover
		raise Exception(f"visit{type(node).__name__} not found")


class Interpreter(NodeVisitor):
	def __init__(self, ast: Node.Program, **kwargs):
		self.ast = ast
		self.stack: Stack = Stack()
		self.fns: list = []
		self.logVisit: bool = kwargs.get("logVisit", False)
		self.logStack: bool = kwargs.get("logStack", False)
		self.logFinal: bool = kwargs.get("logFinal", False)
		self.logAll: bool = kwargs.get("logAll", False)
		if self.logAll is True:  # pragma: no cover
			self.logVisit = True
			self.logStack = True
			self.logFinal = True

		hdlr = logging.StreamHandler(sys.stdout)
		hdlr.setFormatter(logging.Formatter("[ %(name)s ] | %(levelname)s | %(message)s"))
		self.logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")
		self.logger.setLevel(logging.DEBUG)
		self.logger.addHandler(hdlr)

		# FIXME: Hacky way to break loops
		self.breakLoop = False

	def lVisit(self, msg):  # pragma: no cover
		if self.logVisit is True:
			self.logger.info(msg)

	def lStack(self, msg):  # pragma: no cover
		if self.logStack is True:
			self.logger.debug(msg)

	def lFinal(self):  # pragma: no cover
		if self.logFinal is True:
			self.logger.debug(str(self.stack))

	def interpret(self):
		return self.visit(self.ast)

	def visitProgram(self, node: Node.Program):
		self.lVisit("ENTER: Node.Program")

		ar = ActivationRecord(
			node.type,
			ARType.PROGRAM,
			1,
		)
		self.stack.push(ar)

		self.lStack(str(ar))

		for n in node.body:
			self.visit(n)

		self.lVisit("LEAVE: Node.Program")
		self.lStack(str(self.stack))
		self.lFinal()
		return self.stack.pop().members

	# STATEMENTS

	def visitExpressionStatement(self, node: Node.ExpressionStatement):
		self.lVisit("ENTER: Node.ExpressionStatement")
		r = self.visit(node.expression)
		if r == "break":
			self.breakLoop = True
		self.lVisit("LEAVE: Node.ExpressionStatement")

	def visitEmptyStatement(self, _: Node.EmptyStatement):
		pass

	def visitBlockStatement(self, node: Node.BlockStatement):
		self.lVisit("ENTER: Node.BlockStatement")

		returns = []
		for n in node.body:
			r = self.visit(n)
			if r:
				returns.append(r)

		self.lVisit("LEAVE: Node.BlockStatement")

		if len(returns) == 0:  # pragma: no cover
			return
		elif len(returns) == 1:  # pragma: no cover
			return returns[0]
		else:  # pragma: no cover
			return returns

	def visitIfStatement(self, node: Node.IfStatement):
		self.lVisit("ENTER: Node.IfStatement")
		test = self.visit(node.test)
		assert isinstance(test, bool), f'Expected bool, got {type(test).__name__} instead'
		if test is True:
			ret = self.visit(node.consequent)
		else:
			ret = self.visit(node.alternative)
		self.lVisit("LEAVE: Node.IfStatement")
		return ret

	def visitVariableStatement(self, node: Node.VariableStatement):
		self.lVisit("ENTER: Node.VariableStatement")
		for decl in node.declarations:
			self.visit(decl)
		self.lVisit("LEAVE: Node.VariableStatement")

	def visitWhileStatement(self, node: Node.WhileStatement):
		self.lVisit("ENTER: Node.WhileStatement")
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

		self.lVisit("LEAVE: Node.WhileStatement")

	def visitDoWhileStatement(self, node: Node.DoWhileStatement):
		self.lVisit("ENTER: Node.DoWhileStatement")
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

		self.lVisit("LEAVE: Node.DoWhileStatement")

	def visitForStatement(self, node: Node.ForStatement):
		self.lVisit("ENTER: Node.ForStatement")
		tempDecls = []
		if node.init is not None:
			if isinstance(node.init, Node.VariableStatement):
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

		self.lVisit("LEAVE: Node.ForStatement")

	def visitReturnStatement(self, node: Node.ReturnStatement):
		self.lVisit("ENTER: Node.ReturnStatement")
		ret = self.visit(node.argument)
		self.lVisit("LEAVE: Node.ReturnStatement")
		return ret

	# EXPRESSIONS

	def visitComplexExpression(self, node: Node.ComplexExpression):
		self.lVisit("ENTER: Node.ComplexExpression")

		if isinstance(node.left, Node.Identifier):
			left = node.left.name
		else:
			left = self.visit(node.left)

		if isinstance(node.right, Node.Identifier):
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

		if node.type == "BinaryExpression":
			if node.operator == "/":
				assert left is not None, f"Expected value, got None instead"
				assert right is not None, f"Expected value, got None instead"
				try:
					res = eval(f"{lVal} / {rVal}")
				except ZeroDivisionError:
					raise ZeroDivisionError(f"Cannot divide by 0")
				if math.floor(res) == math.ceil(res):
					self.lVisit("LEAVE: Node.ComplexExpression")
					return int(res)
				else:
					self.lVisit("LEAVE: Node.ComplexExpression")
					return float(res)
			else:
				assert left is not None, f"Expected value, got None instead"
				assert right is not None, f"Expected value, got None instead"
				if type(lVal) == str: lVal = f'"{lVal}"'
				if type(rVal) == str: rVal = f'"{rVal}"'
				res = eval(f"{lVal} {node.operator} {rVal}")
				self.lVisit("LEAVE: Node.ComplexExpression")
				return res
		elif node.type == "AssignmentExpression":
			if node.operator == "=":
				ar = self.stack.peek()
				if not ar.varExists(left):
					raise Exception(f'Variable "{left}" does not exist in available scope')

				ar[left] = rVal
			else:
				op = node.operator[0]
				assert lVal is not None, f"Expected value, got None instead"
				assert rVal is not None, f"Expected value, got None instead"
				ar = self.stack.peek()
				if not ar.varExists(left):
					raise Exception(f'Variable "{left}" does not exist in available scope')
				if type(lVal) == str: lVal = f'"{lVal}"'
				if type(rVal) == str: rVal = f'"{rVal}"'
				ar[left] = eval(f"{lVal} {op} {rVal}")
		elif node.type == "LogicalExpression":
			if node.operator == "&&":
				operator = "and"
			elif node.operator == "||":
				operator = "or"
			else:  # pragma: no cover
				# **should** not happen
				raise Exception(f"Unknown operator in Logical Expression: {node.operator}")
			return eval(f"{left} {operator} {right}", self.stack.peek().members)
		elif node.type == "BitwiseExpression":
			assert left is not None, f"Expected value, got None instead"
			assert right is not None, f"Expected value, got None instead"
			return eval(f"{left} {node.operator} {right}")
		else:  # pragma: no cover
			raise Exception(f"Unknown ComplexExpression: {node}")
		self.lVisit("LEAVE: Node.ComplexExpression")

	def visitUnaryExpression(self, node: Node.UnaryExpression):
		self.lVisit("ENTER: Node.UnaryExpression")
		val = self.visit(node.argument)
		if val is None:
			raise Exception(f'Cannot use {node.operator} on "null"')
		else:
			if node.operator == "!":
				val = eval(f"not {val}", self.stack.peek().members)
			else:
				val = eval(f"{node.operator}{val}", self.stack.peek().members)
		self.lVisit("LEAVE: Node.UnaryExpression")
		return val

	def visitCallExpression(self, node: Node.CallExpression):
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
			if isinstance(argName, Node.Identifier):
				ar[argName.name] = self.visit(argValue)
			else:
				ar[argName] = self.visit(argValue)

		self.stack.push(ar)
		self.lVisit(f"ENTER: Node.CallExpression({node.callee.name}, {ar.members})")
		self.lStack(str(self.stack))

		f = node.fn.get("body", None)
		assert f is not None, f'Failed to aquire function body for "{node.callee.name}"'

		ret = self.visit(f)

		self.lVisit(f"LEAVE: Node.CallExpression({node.callee.name})")
		self.lStack(str(self.stack))
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

	def visitVariableDeclaration(self, node: Node.VariableDeclaration):
		varName = self.visit(node.id)
		varValue = self.visit(node.init)
		_vv = f'"{varValue}"' if type(varValue) == str else varValue
		self.lVisit(f"ENTER: Node.VariableDeclaration({varName}, {_vv})")
		ar = self.stack.peek()
		if ar.varExists(varName):
			raise Exception(f'Variable "{varName}" already exists in available scope')
		elif type(varName) != str:
			raise Exception(f'Unknown variable "{varName}"')
		ar[varName] = varValue
		self.lVisit(f"LEAVE: Node.VariableDeclaration({varName}, {_vv})")
		del _vv

	def visitFunctionDeclaration(self, node: Node.FunctionDeclaration):
		self.lVisit(f"ENTER: Node.FunctionDeclaration({node.name.name})")
		if node.name.name in self.fns:
			raise Exception(f'Function "{node.name.name}" already exists in available scope')
		self.fns.append(node.name.name)
		self.lVisit(f"LEAVE: Node.FunctionDeclaration({node.name.name})")

	# def visitClassDeclaration(self, node: Node.ClassDeclaration):
	# 	self.lVisit("ENTER: Node.ClassDeclaration")
	# 	self.lVisit("LEAVE: Node.ClassDeclaration")

	# OTHER

	def visitIdentifier(self, node: Node.Identifier):
		self.lVisit("ENTER: Node.Identifier")
		if self.stack.peek().varExists(node.name):
			val = self.stack.peek().members.get(node.name)
		else:
			val = node.name
		self.lVisit("LEAVE: Node.Identifier")
		return val

	def visitLiteral(self, node: Node.Literal):
		self.lVisit("ENTER: Node.Literal")
		self.lVisit("LEAVE: Node.Literal")
		return node.value
