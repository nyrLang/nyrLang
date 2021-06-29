import math
from typing import Any

import Nyr.Parser.Node as Node
from Nyr.Interpreter.Env import Env


class Interpreter:
	blockId: int = 0

	def interpret(self, node: Node.Node, env: Env) -> Any:

		if node is None: return None
		elif isinstance(node, Node.Program):
			for child in node.body:
				self.interpret(child, env)
			return env
		elif isinstance(node, Node.VariableDeclaration):
			id_ = self.interpret(node.id, env)
			if node.init is None:
				value = None
			else:
				value = self.interpret(node.init, env)

			env.addVar(id_, value)
		elif isinstance(node, Node.Identifier): return node.name
		elif isinstance(node, Node.ExpressionStatement): return self.interpret(node.expression, env)
		elif isinstance(node, Node.EmptyStatement): return
		elif isinstance(node, Node.BlockStatement):
			e = Env(parent=env)

			for part in node.body:
				self.interpret(part, e)

			return env.addChildEnv(f"__block_{self.blockId}", e)
		# elif isinstance(node, Node.IfStatement):
		elif isinstance(node, Node.VariableStatement):
			for decl in node.declarations:
				self.interpret(decl, env)
		# elif isinstance(node, Node.WhileStatement):
		# elif isinstance(node, Node.ForStatement):
		elif isinstance(node, Node.ComplexExpression):
			if node.type == "AssignmentExpression":
				left = self.interpret(node.left, env)
				right = self.interpret(node.right, env)

				env.setVar(left, right)
			elif node.type in ["BinaryExpression", "LogicalExpression"]:
				operator = node.operator

				left = self.interpret(node.left, env)
				if not isinstance(node.left, Node.Literal):
					if node.left.type in [int, float]:
						left = node.left.value
					else:
						left = env.getVar(left)

				right = self.interpret(node.right, env)
				if not isinstance(node.right, Node.Literal):
					if node.right.type in [int, float]:
						right = node.right.value
					else:
						right = env.getVar(right)

				try:
					e = eval(f"{left} {operator} {right}")
					if int(e) == e:
						return int(e)
					else:
						return float(e)
				except TypeError:
					raise RuntimeError(f"BinaryExpression '{operator}' with '{left}' and '{right}' was not possible")
				except Exception as e:
					raise e
			else: pass
		elif isinstance(node, Node.UnaryExpression):
			operator = node.operator
			assert isinstance(node.argument, Node.Literal), f"Argument of UnaryExpression should be of type 'Literal'; but {node.argument.type} was recieved"
			assert node.argument.type in ["IntegerLiteral", "FloatLiteral"], f"Argument of UnaryExpression should be of type 'Integer' or 'Float'; but {node.argument.type} was recieved"

			value = self.interpret(node.argument, env)

			try:
				return eval(f"{operator}{value}")
			except Exception as e:
				raise e
		# elif isinstance(node, Node.FunctionDeclaration):
		# elif isinstance(node, Node.ReturnStatement):
		# elif isinstance(node, Node.CallExpression):
		# elif isinstance(node, Node.ClassDeclaration):
		# elif isinstance(node, Node.Super):
		# elif isinstance(node, Node.ThisExpression):
		# elif isinstance(node, Node.NewExpression):
		elif isinstance(node, Node.Literal): return node.value
		else: raise RuntimeError(f"{node.type} is not yet implemented.")

		self.blockId += 1


class SExprInterpreter:
	ast: list

	def __init__(self, ast: list):
		self.ast = ast
		self.globalObj: dict[str, Any] = {}

	def interpret(self):
		raise Exception(f"S-Expression interpreter is not yet implemented!")
