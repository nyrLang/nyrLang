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
			id_ = self.interpret(node.id)
			if node.init is None:
				value = None
			else:
				if isinstance(node.init, Node.Literal):
					value = node.init.value
				elif isinstance(node.init, Node.UnaryExpression):
					value = self.interpret(node.init)
				elif isinstance(node.init, Node.ComplexExpression):
					raise RuntimeError(f"Assigning from {node.init.type} is not yet implemented")
				else:
					raise RuntimeError(f"Unknown right-hand-side of variable declaration ({id_})")

			if id_ in self.globalObj.keys():
				raise RuntimeError(f"Variable '{id_}' already initialized")
			self.globalObj[id_] = value
		elif isinstance(node, Node.Identifier): return node.name
		elif isinstance(node, Node.ExpressionStatement): return self.interpret(node.expression)
		elif isinstance(node, Node.EmptyStatement): return
		elif isinstance(node, Node.BlockStatement):
			for part in node.body:
				self.interpret(part)
		elif isinstance(node, Node.IfStatement): pass
		elif isinstance(node, Node.VariableStatement):
			for decl in node.declarations:
				self.interpret(decl)
		elif isinstance(node, Node.WhileStatement): pass
		elif isinstance(node, Node.ForStatement): pass
		elif isinstance(node, Node.ComplexExpression):
			if node.type == "AssignmentExpression":
				left = self.interpret(node.left)
				right = self.interpret(node.right)

				if left not in self.globalObj:
					raise RuntimeError(f"Variable '{left}' has not been defined")
				self.globalObj[left] = right
				return
			elif node.type in ["BinaryExpression", "LogicalExpression"]:
				operator = node.operator
				if isinstance(node.left, Node.Identifier):
					if node.left.name not in self.globalObj:
						raise RuntimeError(f"'{node.left.name}' accessed before defined")
					left = self.globalObj[node.left.name]
					if left is None:
						raise RuntimeError(f"'{node.left.name}' has no value")
				else: left = self.interpret(node.left)

				if isinstance(node.right, Node.Identifier):
					if node.right.name not in self.globalObj:
						raise RuntimeError(f"'{node.right.name}' accessed before defined")
					right = self.globalObj[node.right.name]
					if right is None:
						raise RuntimeError(f"'{node.right.name}' has no value")
				else: right = self.interpret(node.right)

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

			value = self.interpret(node.argument)

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
		else: raise RuntimeError(f"{node.type} is not yet implemented.")


class SExprInterpreter:
	ast: list

	def __init__(self, ast: list):
		self.ast = ast
		self.globalObj: dict[str, Any] = {}

	def interpret(self):
		raise Exception(f"S-Expression interpreter is not yet implemented!")
