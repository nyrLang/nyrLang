import logging
import math
import sys
from collections.abc import Callable

from nyr.interpreter.stack import ActivationRecord
from nyr.interpreter.stack import ARType
from nyr.interpreter.stack import Stack
from nyr.parser import node as Node

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
	ast: Node.Program
	stack: Stack
	fns: list = []

	def __init__(self, logVisit: bool = False, logStack: bool = False, logFinal: bool = False):
		self._logVisit = logVisit
		self._logStack = logStack
		self._logFinal = logFinal

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
		if self._logVisit:
			self.logger.info(msg)

	def logStack(self, msg):  # pragma: no cover
		if self._logStack:
			self.logger.debug(msg)

	def logFinal(self):  # pragma: no cover
		if self._logFinal:
			self.logger.debug(str(self.stack))

	def interpret(self, ast: Node.Program):
		self._reset()
		return self.visit(ast)

	def visitProgram(self, node: Node.Program):
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

	def visitExpressionStatement(self, node: Node.ExpressionStatement):
		self.logVisit("ENTER: Node.ExpressionStatement")
		r = self.visit(node.expression)
		if r == "break":
			self.breakLoop = True
		self.logVisit("LEAVE: Node.ExpressionStatement")

	def visitEmptyStatement(self, _: Node.EmptyStatement):
		pass

	def visitBlockStatement(self, node: Node.BlockStatement):
		self.logVisit("ENTER: Node.BlockStatement")

		returns = []
		for n in node.body:
			r = self.visit(n)
			if r is not None:
				returns.append(r)

		self.logVisit("LEAVE: Node.BlockStatement")

		if len(returns) == 0:  # pragma: no cover
			return
		elif len(returns) == 1:  # pragma: no cover
			return returns[0]
		else:  # pragma: no cover
			return returns

	def visitIfStatement(self, node: Node.IfStatement):
		self.logVisit("ENTER: Node.IfStatement")
		test = self.visit(node.test)
		assert isinstance(test, bool), f"Expected bool, got {type(test).__name__} instead"
		ret = self.visit(node.consequent if test else node.alternative)
		self.logVisit("LEAVE: Node.IfStatement")
		return ret

	def visitVariableStatement(self, node: Node.VariableStatement):
		self.logVisit("ENTER: Node.VariableStatement")
		for decl in node.declarations:
			self.visit(decl)
		self.logVisit("LEAVE: Node.VariableStatement")

	def visitWhileStatement(self, node: Node.WhileStatement):
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
				raise RecursionError(f"Exceeded {MAXITERATIONS} iterations in while statement")

			# FIXME: hacky way to break loops
			if self.breakLoop is True:
				self.breakLoop = False
				break

		self.logVisit("LEAVE: Node.WhileStatement")

	def visitDoWhileStatement(self, node: Node.DoWhileStatement):
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
				raise RecursionError(f"Exceeded {MAXITERATIONS} iterations in do-while statement")

			# FIXME: hacky way to break loops
			if self.breakLoop is True:
				self.breakLoop = False
				break

		self.logVisit("LEAVE: Node.DoWhileStatement")

	def visitForStatement(self, node: Node.ForStatement):
		self.logVisit("ENTER: Node.ForStatement")
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
				raise RecursionError(f"Exceeded {MAXITERATIONS} iterations in for statement")

			# FIXME: hacky way to break loops
			if self.breakLoop is True:
				self.breakLoop = False
				break

		for decl in tempDecls:
			del self.stack.peek().members[decl]
		del tempDecls

		self.logVisit("LEAVE: Node.ForStatement")

	def visitReturnStatement(self, node: Node.ReturnStatement):
		self.logVisit("ENTER: Node.ReturnStatement")
		ret = self.visit(node.argument)
		self.logVisit("LEAVE: Node.ReturnStatement")
		return ret

	# EXPRESSIONS

	def _binaryExpression(self, **kwargs):
		lVal = kwargs.get("lVal")
		rVal = kwargs.get("rVal")
		op = kwargs.get("op")

		assert lVal is not None, "Expected value, got None instead"
		assert rVal is not None, "Expected value, got None instead"

		if op == "/":
			try:
				res = eval(f"{lVal} / {rVal}")
			except ZeroDivisionError:
				raise ZeroDivisionError("Cannot divide by 0")

			if math.floor(res) == math.ceil(res):
				_res = int(res)
			else:
				_res = float(res)
		else:
			if type(lVal) == str:
				lVal = f'"{lVal}"'
			if type(rVal) == str:
				rVal = f'"{rVal}"'

			_res = eval(f"{lVal} {op} {rVal}")

		return _res

	def _assignmentExpression(self, **kwargs):
		left = kwargs.get("left")
		lVal = kwargs.get("lVal")
		rVal = kwargs.get("rVal")
		op = kwargs.get("op")

		ar = self.stack.peek()
		if not ar.varExists(left):
			raise NameError(f'Variable "{left}" does not exist in available scope')

		if op != "=":
			op = op[0]
			assert lVal is not None, "Expected value, got None instead"
			assert rVal is not None, "Expected value, got None instead"

			if type(lVal) == str:
				lVal = f'"{lVal}"'
			if type(rVal) == str:
				rVal = f'"{rVal}"'

			rVal = eval(f"{lVal} {op} {rVal}")

		ar[left] = rVal

	def _logicalExpression(self, **kwargs):
		lVal = kwargs.get("lVal")
		rVal = kwargs.get("rVal")
		op = kwargs.get("op")

		try:
			operator = {"&&": "and", "||": "or"}[op]
		except KeyError:  # pragma: no cover
			# **should** not happen
			raise SyntaxError(f"Unknown operator in Logical Expression: {op}")
		return eval(f"{lVal} {operator} {rVal}")

	def _bitwiseExpression(self, **kwargs):
		lVal = kwargs.get("lVal")
		rVal = kwargs.get("rVal")
		op = kwargs.get("op")

		assert lVal is not None, "Expected value, got None instead"
		assert rVal is not None, "Expected value, got None instead"
		return eval(f"{lVal} {op} {rVal}")

	def visitComplexExpression(self, node: Node.ComplexExpression):
		self.logVisit("ENTER: Node.ComplexExpression")

		if isinstance(node.left, Node.Identifier):
			left = node.left.name
		else:
			left = self.visit(node.left)

		if isinstance(node.right, Node.Identifier):
			right = node.right.name
		else:
			right = self.visit(node.right)

		if type(left) == str:
			peek = self.stack.peek()
			if peek.varExists(left):
				lVal = peek.get(left)
			else:
				lVal = f'{left}'
		else:
			lVal = left

		if type(right) == str:
			peek = self.stack.peek()
			if peek.varExists(right):
				rVal = peek.get(right)
			else:
				rVal = f'{right}'
		else:
			rVal = right

		if left is None:  # pragma: no cover
			raise Exception(f"Unknown left-hand side of ComplexExpression: {node.left}")
		if right is None:  # pragma: no cover
			raise Exception(f"Unknown right-hand side of ComplexExpression: {node.right}")

		_res = None

		try:
			_res = {
				"BinaryExpression": self._binaryExpression,
				"AssignmentExpression": self._assignmentExpression,
				"LogicalExpression": self._logicalExpression,
				"BitwiseExpression": self._bitwiseExpression,
			}[node.type](
				op=node.operator,
				left=left,
				lVal=lVal,
				rVal=rVal,
			)
		except KeyError:  # pragma: no cover
			raise Exception(f"Unknown ComplexExpression: {node}")

		self.logVisit("LEAVE: Node.ComplexExpression")
		return _res

	def visitUnaryExpression(self, node: Node.UnaryExpression):
		self.logVisit("ENTER: Node.UnaryExpression")
		val = self.visit(node.argument)
		if val is None:
			raise SyntaxError(f'Cannot use {node.operator} on "null"')
		else:
			if node.operator == "!":
				val = eval(f"not {val}", self.stack.peek().members)
			else:
				val = eval(f"{node.operator}{val}", self.stack.peek().members)
		self.logVisit("LEAVE: Node.UnaryExpression")
		return val

	def visitCallExpression(self, node: Node.CallExpression):
		if node.callee.name not in self.fns:
			raise NameError(f'Function "{node.callee.name}" does not exist in available scope')
		if node.fn is None:  # pragma: no cover
			raise Exception(f'Failed to aquire function for "{node.callee.name}"')
		if len(node.arguments) != len(node.fn.get("args")):
			raise Exception(f"Incorrect amount of arguments given. Expected {len(node.fn.get('args'))}, got {len(node.arguments)}")

		ar = ActivationRecord(
			node.type,
			ARType.FUNCTION,
			self.stack.peek().nestingLevel + 1,
		)
		if ar.nestingLevel > MAXRECURSIONDEPTH:
			raise RecursionError(f'Exceeded recursion depth of {MAXRECURSIONDEPTH} in function "{node.callee.name}"')
		for argName, argValue in zip(node.fn.get("args", {}), node.arguments):
			if isinstance(argName, Node.Identifier):
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

	def visitVariableDeclaration(self, node: Node.VariableDeclaration):
		varName = self.visit(node.id)
		varValue = self.visit(node.init)
		_vv = f'"{varValue}"' if type(varValue) == str else varValue
		self.logVisit(f"ENTER: Node.VariableDeclaration({varName}, {_vv})")
		ar = self.stack.peek()
		if ar.varExists(varName):
			# FIXME: Does not happen for some reason
			raise NameError(f'Variable "{varName}" already exists in available scope')
		elif type(varName) != str:
			raise NameError(f'Unknown variable "{varName}"')
		ar[varName] = varValue
		self.logVisit(f"LEAVE: Node.VariableDeclaration({varName}, {_vv})")
		del _vv

	def visitFunctionDeclaration(self, node: Node.FunctionDeclaration):
		nodeName = node.name.name
		self.logVisit(f"ENTER: Node.FunctionDeclaration({nodeName})")
		if nodeName in self.fns:
			raise NameError(f'Function "{nodeName}" already exists in available scope')
		self.fns.append(nodeName)
		self.logVisit(f"LEAVE: Node.FunctionDeclaration({nodeName})")

	# def visitClassDeclaration(self, node: Node.ClassDeclaration):
	# 	self.lVisit("ENTER: Node.ClassDeclaration")
	# 	self.lVisit("LEAVE: Node.ClassDeclaration")

	# OTHER

	def visitIdentifier(self, node: Node.Identifier):
		self.logVisit("ENTER: Node.Identifier")
		peek = self.stack.peek()
		if peek.varExists(node.name):
			val = peek.members.get(node.name)
		else:
			val = node.name
		self.logVisit("LEAVE: Node.Identifier")
		return val

	def visitLiteral(self, node: Node.Literal):
		self.logVisit("ENTER: Node.Literal")
		self.logVisit("LEAVE: Node.Literal")
		return node.value
