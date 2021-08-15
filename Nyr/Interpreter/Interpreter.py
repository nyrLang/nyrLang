from typing import Any

from Nyr.Interpreter.Env import Env
from Nyr.Parser import Node


class Interpreter:
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

			if name in env.keys():
				raise Exception(f"Variable '{name}' has already been declared")
			val = None
			if node.init is not None:
				val = self.interpret(node.init, env)

			env[name] = val
		elif isinstance(node, Node.Identifier):
			return node.name
		elif isinstance(node, Node.ExpressionStatement):
			self.interpret(node.expression, env)
		elif isinstance(node, Node.EmptyStatement):
			pass
		elif isinstance(node, Node.BlockStatement):
			for n in node.body:
				self.interpret(n, env)
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
		# elif isinstance(node, Node.WhileStatement):pass
		# elif isinstance(node, Node.ForStatement):pass
		elif isinstance(node, Node.ComplexExpression):
			left = self.interpret(node.left, env)
			right = self.interpret(node.right, env)

			if left is None: raise Exception(f"Unknown left-hand side of AssignmentExpression")
			if right is None: raise Exception(f"Unknown right-hand side of AssignmentExpression")

			if node.type == "BinaryExpression":
				return eval(f"{left} {node.operator} {right}", env)
			elif node.type == "AssignmentExpression":
				if node.operator == "=":
					left = self.interpret(node.left, env)
					right = self.interpret(node.right, env)

					if left is None:
						raise Exception(f"Unknown left-hand side of AssignmentExpression")
					if right is None:
						raise Exception(f"Unknown right-hand side of AssignmentExpression")

					if left not in env.keys():
						raise Exception(f"Variable {left} accessed before declaration")
					env[left] = right
				else:
					op = node.operator[0]
					exec(f"{left} = {left} {op} {right}", env)
			else: raise Exception(f"Unknown ComplexExpression: {node.type}")
		elif isinstance(node, Node.UnaryExpression):
			val = self.interpret(node.argument, env)
			return eval(f"{node.operator}{val}", env)
		# elif isinstance(node, Node.FunctionDeclaration):pass
		# elif isinstance(node, Node.ReturnStatement):pass
		# elif isinstance(node, Node.CallExpression):pass
		# elif isinstance(node, Node.ClassDeclaration):pass
		# elif isinstance(node, Node.Super):pass
		# elif isinstance(node, Node.ThisExpression):pass
		# elif isinstance(node, Node.NewExpression):pass
		elif isinstance(node, Node.Literal):
			return node.value
		else:
			raise NotImplementedError(f"{str(type(node)).split('.')[-1][:-2]} ({node.type}) is not yet implemented.")
