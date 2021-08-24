import math
from typing import Any

from Nyr.Interpreter.Env import Env
from Nyr.Parser import Node

MAXITERATIONS = 2 ** 16
# TODO: find a way to implement this
RECURSIONDEPTH = 256


class Interpreter:
	# FIXME: Hacky way to break loops
	breakLoop = False

	def interpret(self, node: Node.Node, env: Env) -> Any:
		if node is None: return None

		if isinstance(node, Node.Program):
			for n in node.body:
				self.interpret(n, env)
			if "__builtins__" in env.keys():
				del env["__builtins__"]
			return env
		elif isinstance(node, Node.VariableDeclaration):
			name = self.interpret(node.id, env)

			val = None
			if node.init is not None:
				val = self.interpret(node.init, env)

			env.addValue(name, val)
		elif isinstance(node, Node.Identifier):
			return node.name
		elif isinstance(node, Node.ExpressionStatement):
			r = self.interpret(node.expression, env)
			if r == "break":
				self.breakLoop = True
		elif isinstance(node, Node.EmptyStatement):
			pass
		elif isinstance(node, Node.BlockStatement):
			returns = []
			for n in node.body:
				r = self.interpret(n, env)
				if r is not None:
					returns.append(r)
			if len(returns) == 0:  # pragma: no cover
				return None
			elif len(returns) == 1:  # pragma: no cover
				return returns[0]
			else:  # pragma: no cover
				return returns
		elif isinstance(node, Node.IfStatement):
			test = self.interpret(node.test, env)
			assert isinstance(test, bool)
			if test is True:
				self.interpret(node.consequent, env)
			else:
				self.interpret(node.alternative, env)
		elif isinstance(node, Node.VariableStatement):
			for decl in node.declarations:
				self.interpret(decl, env)
		elif isinstance(node, Node.WhileStatement):
			test = self.interpret(node.test, env)
			assert isinstance(test, bool)

			iterations = 0
			while test is True:
				self.interpret(node.body, env)
				test = self.interpret(node.test, env)

				iterations += 1

				if iterations > MAXITERATIONS:
					raise Exception(f"Exceeded {MAXITERATIONS} iterations in while statement")

				# FIXME: hacky way to break loops
				if self.breakLoop is True:
					self.breakLoop = False
					break
		elif isinstance(node, Node.DoWhileStatement):
			self.interpret(node.body, env)
			test = self.interpret(node.test, env)
			assert isinstance(test, bool)

			iterations = 0
			while test is True:
				self.interpret(node.body, env)
				test = self.interpret(node.test, env)

				iterations += 1

				if iterations > MAXITERATIONS:
					raise Exception(f"Exceeded {MAXITERATIONS} iterations in do-while statement")

				# FIXME: hacky way to break loops
				if self.breakLoop is True:
					self.breakLoop = False
					break
		elif isinstance(node, Node.ForStatement):
			forEnv = Env(parent=env)
			self.interpret(node.init, forEnv)
			test = True
			if node.test is not None:
				test = self.interpret(node.test, forEnv)
				assert isinstance(test, bool), f"Interpreter::Node.ForStatement: Expected bool, got {type(test)} instead"

			iterations = 0
			while test is True:
				self.interpret(node.body, forEnv)

				self.interpret(node.update, forEnv)
				if node.test is not None:
					test = self.interpret(node.test, forEnv)
					assert isinstance(test, bool), f"Interpreter::Node.ForStatement: Expected bool, got {type(test)} instead"
				iterations += 1

				if iterations > MAXITERATIONS:
					raise Exception(f"Exceeded {MAXITERATIONS} iterations in for statement")

				# FIXME: hacky way to break loops
				if self.breakLoop is True:
					self.breakLoop = False
					break
			del forEnv
		elif isinstance(node, Node.ComplexExpression):
			left = self.interpret(node.left, env)
			right = self.interpret(node.right, env)

			if left is None:  # pragma: no cover
				raise Exception(f"Unknown left-hand side of ComplexExpression: {node.left}")
			if right is None:  # pragma: no cover
				raise Exception(f"Unknown right-hand side of ComplexExpression: {node.right}")

			lVal = left
			rVal = right
			if type(left) == str:
				if env.findOwner(left) is not None:
					lVal = env.getValue(left)
				else:
					lVal = f'"{lVal}"'

			if type(right) == str:
				if env.findOwner(right) is not None:
					rVal = env.getValue(right)
				else:
					rVal = f'"{rVal}"'

			if node.type == "BinaryExpression":
				if node.operator == "/":
					assert lVal is not None, f"Expected value, got None instead"
					assert rVal is not None, f"Expected value, got None instead"
					res = eval(f"{lVal} / {rVal}", env)
					if math.floor(res) == math.ceil(res):
						return int(res)
					else:
						return float(res)
				else:
					assert lVal is not None, f"Expected value, got None instead"
					assert rVal is not None, f"Expected value, got None instead"
					return eval(f"{lVal} {node.operator} {rVal}")
			elif node.type == "AssignmentExpression":
				if node.operator == "=":
					left = self.interpret(node.left, env)
					right = self.interpret(node.right, env)

					if left is None:  # pragma: no cover
						raise Exception(f"Unknown left-hand side of AssignmentExpression: {node.left}")
					if right is None:  # pragma: no cover
						raise Exception(f"Unknown right-hand side of AssignmentExpression: {node.right}")

					env.setValue(left, right)
				else:
					op = node.operator[0]
					assert lVal is not None, f"Expected value, got None instead"
					assert rVal is not None, f"Expected value, got None instead"
					env.setValue(left, eval(f"{lVal} {op} {rVal}"))
			elif node.type == "LogicalExpression":
				if node.operator == "&&":
					operator = "and"
				elif node.operator == "||":
					operator = "or"
				else:  # pragma: no cover
					# **should** not happen
					raise Exception(f"Unknown operator in Logical Expression: {node.operator}")
				return eval(f"{left} {operator} {right}", env)
			else:  # pragma: no cover
				raise Exception(f"Unknown ComplexExpression: {node}")
		elif isinstance(node, Node.UnaryExpression):
			val = self.interpret(node.argument, env)
			return eval(f"{node.operator}{val}", env)
		elif isinstance(node, Node.FunctionDeclaration):
			args = []
			for arg in node.params:
				assert isinstance(arg, Node.Identifier)
				args.append(arg.name)
			env.addFunc(node.name.name, {"args": args, "body": node.body})
		elif isinstance(node, Node.ReturnStatement):
			return self.interpret(node.argument, env)
		elif isinstance(node, Node.CallExpression):
			func = env.getFunc(node.callee.name)
			if len(node.arguments) != len(func.get("args", -1)):
				raise Exception(f"Incorrect amount of arguments given. Expected {len(func.get('args'))}, got {len(node.arguments)}")

			funcEnv = Env(parent=env)
			for i in range(len(node.arguments)):
				funcEnv.addValue(
					# FIXME: Another hack
					self.interpret(Node.Identifier(func.get("args")[i]), funcEnv),
					funcEnv.getValue(self.interpret(node.arguments[i], funcEnv)),
				)
			return self.interpret(func.get("body"), funcEnv)
		# elif isinstance(node, Node.ClassDeclaration):pass
		# elif isinstance(node, Node.Super):pass
		# elif isinstance(node, Node.ThisExpression):pass
		# elif isinstance(node, Node.NewExpression):pass
		elif isinstance(node, Node.Literal):
			return node.value
		else:  # pragma: no cover
			assert isinstance(node, Node.Node), f"Got {type(node)} instead of Node. Value: {node}"
			raise NotImplementedError(f"{str(type(node)).split('.')[-1][:-2]} ({node.type}) is not yet implemented.")
