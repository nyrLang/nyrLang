from typing import Any

import Nyr.Parser.Node as Node


class Interpreter:
	def __init__(self, ast: Node.Program = None):
		self.globalObj: dict[str, Any] = {}

		if ast is not None:
			self.interpret(ast)

	def interpret(self, node: Node.Node) -> Any:
		if isinstance(node, Node.Program):
			for child in node.body:
				self.interpret(child)
			return self.globalObj
		elif isinstance(node, Node.VariableDeclaration):
			assert isinstance(node.id, Node.Identifier)
			if node.id.name not in self.globalObj:
				self.globalObj[node.id.name] = None

			if node.init is not None:
				self.globalObj[node.id.name] = self.interpret(node.init)
		elif isinstance(node, Node.Identifier): pass

		# Statements
		elif isinstance(node, Node.ExpressionStatement): return self.interpret(node.expression)
		elif isinstance(node, Node.EmptyStatement): pass
		elif isinstance(node, Node.VariableStatement):
			for declaration in node.declarations:
				self.interpret(declaration)

		# ComplexExpressions
		elif isinstance(node, Node.ComplexExpression):
			if node.type == "BinaryExpression":
				left = self.interpret(node.left)
				right = self.interpret(node.right)
				if isinstance(node.left, Node.Identifier):
					left = self.globalObj[node.left.name]
				if isinstance(node.right, Node.Identifier):
					right = self.globalObj[node.right.name]

				try:
					return eval(f"{left} {node.operator} {right}")
				except TypeError:
					if left is None:
						print(f"Variable '{node.left.name}' is uninitialized")
					if right is None:
						print(f"Variable '{node.right.name}' is uninitialized")
					return
				except Exception as e:
					raise e
			elif node.type == "AssignmentExpression":
				if not isinstance(node.left, Node.Identifier):
					raise RuntimeError(f"Cannot assign to {node.left.type}")
				if node.left.name not in self.globalObj:
					raise RuntimeError(f"Variable {node.left.name} has not bee initialized")
				self.globalObj[node.left.name] = self.interpret(node.right)
			else: raise RuntimeError(f"ComplexExpression of type '{node.type}' has not been implemented")
		elif isinstance(node, Node.Literal): return node.value

		else: raise RuntimeError(f"{node.type} is not yet implemented.")
