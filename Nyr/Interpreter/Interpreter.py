from typing import Any

import Nyr.Parser.Node as Node
from Nyr.Interpreter.Env import Env


class Interpreter:
	blockId: int = 0

	def interpret(self, node: Node.Node, env: Env, blockName=None) -> Any:
		if blockName is None:
			blockName = f"__block_{self.blockId}"
			self.blockId += 1

		if isinstance(node, Node.Program):
			for child in node.body:
				self.interpret(child, env)
			return env
		elif isinstance(node, Node.VariableDeclaration):
			id_ = self.interpret(node.id, env)
			if node.init is None:
				value = None
			else:
				if isinstance(node.init, Node.Literal):
					value = node.init.value
				elif isinstance(node.init, Node.UnaryExpression):
					value = self.interpret(node.init, env)
				elif isinstance(node.init, Node.ComplexExpression):
					raise RuntimeError(f"Assigning from {node.init.type} is not yet implemented")
				else:
					raise RuntimeError(f"Unknown right-hand-side of variable declaration ({id_})")

			try:
				if id_ in env.find(id_):
					env.find(id_)[id_] = value
			except AttributeError:
				env[id_] = value
			except Exception as e:
				raise e
			return
		elif isinstance(node, Node.Identifier): return node.name
		elif isinstance(node, Node.ExpressionStatement): return self.interpret(node.expression, env)
		elif isinstance(node, Node.EmptyStatement): return
		elif isinstance(node, Node.BlockStatement):
			e = Env(parent=env)

			for part in node.body:
				self.interpret(part, e)

			return env.addChild(blockName, e)
		elif isinstance(node, Node.IfStatement): pass
		elif isinstance(node, Node.VariableStatement):
			for decl in node.declarations:
				self.interpret(decl, env)
			return
		elif isinstance(node, Node.WhileStatement): pass
		elif isinstance(node, Node.ForStatement): pass
		elif isinstance(node, Node.ComplexExpression):
			if node.type == "AssignmentExpression":
				left = self.interpret(node.left, env)
				right = self.interpret(node.right, env)

				try:
					env.find(left)[left] = right
					return
				except AttributeError:
					raise RuntimeError(f"Variable '{left}' has not been defined")
				except Exception as e:
					raise e
			elif node.type in ["BinaryExpression", "LogicalExpression"]:
				operator = node.operator
				if isinstance(node.left, Node.Identifier):
					try:
						left = env.find(node.left.name)
					except AttributeError:
						raise RuntimeError(f"'{node.left.name}' accessed before defined")
					except Exception as e:
						raise e
					if left is None:
						raise RuntimeError(f"'{node.left.name}' has no value")
				else: left = self.interpret(node.left, env)

				if isinstance(node.right, Node.Identifier):
					try:
						right = env.find(node.right.name)
					except AttributeError:
						raise RuntimeError(f"'{node.right.name}' accessed before defined")
					except Exception as e:
						raise e
					if right is None:
						raise RuntimeError(f"'{node.right.name}' has no value")
				else: right = self.interpret(node.right, env)

				try:
					return eval(f"{left} {operator} {right}")
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
		elif isinstance(node, Node.FunctionDeclaration): pass
		elif isinstance(node, Node.ReturnStatement): pass
		elif isinstance(node, Node.CallExpression): pass
		elif isinstance(node, Node.ClassDeclaration): pass
		elif isinstance(node, Node.Super): pass
		elif isinstance(node, Node.ThisExpression): pass
		elif isinstance(node, Node.NewExpression): pass
		elif isinstance(node, Node.Literal): return node.value

		raise RuntimeError(f"{node.type} is not yet implemented.")


class SExprInterpreter:
	ast: list

	def __init__(self, ast: list):
		self.ast = ast
		self.globalObj: dict[str, Any] = {}

	def interpret(self):
		raise Exception(f"S-Expression interpreter is not yet implemented!")
