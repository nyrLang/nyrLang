from typing import Any

from Nyr.Interpreter.Env import Env
from Nyr.Parser import Node


class Interpreter:
	def interpret(self, node: Node.Node, env: Env) -> Any:
		if node is None: return None

		match type(node):
			case Node.Program:
				assert isinstance(node, Node.Program)
				for b in node.body:
					self.interpret(b, env)
				return env
			case Node.VariableDeclaration:
				assert isinstance(node, Node.VariableDeclaration)
				assert isinstance(node.id, Node.Identifier)
				varName = self.interpret(node.id, env)

				varValue = node.init
				if varValue is not None:
					if isinstance(varValue, Node.Identifier):
						varValue = env.findOwner(varValue.name)[varValue.name]
					elif isinstance(varValue, Node.Literal):
						varValue = self.interpret(varValue, env)
					else:
						raise Exception(f"Unknow right-hand-side of {node.type}")
				env.update({varName: varValue})
			case Node.Identifier:
				assert isinstance(node, Node.Identifier)
				return node.name
			case Node.ExpressionStatement:
				assert isinstance(node, Node.ExpressionStatement)
				self.interpret(node.expression, env)
			# case Node.EmptyStatement:
			# 	assert isinstance(node, Node.EmptyStatement)
			# case Node.BlockStatement:
			# 	assert isinstance(node, Node.BlockStatement)
			# case Node.IfStatement:
			# 	assert isinstance(node, Node.IfStatement)
			case Node.VariableStatement:
				assert isinstance(node, Node.VariableStatement)
				for decl in node.declarations:
					self.interpret(decl, env)
			# case Node.WhileStatement:
			# 	assert isinstance(node, Node.WhileStatement)
			# case Node.ForStatement:
			# 	assert isinstance(node, Node.ForStatement)
			case Node.ComplexExpression:
				assert isinstance(node, Node.ComplexExpression)
				match node.type:
					case "AssignmentExpression":
						assert isinstance(node.left, Node.Identifier)
						assert type(node.right) in [Node.Identifier, Node.Literal]

						if isinstance(node.right, Node.Identifier):
							if node.right.name not in env:
								raise Exception(f"Variable {node.right.name} does not exist")
							value = env.findOwner(node.right.name)[node.right.name]
						else:
							assert isinstance(node.right, Node.Literal)
							value = self.interpret(node.right, env)

						env.update({node.left.name: value})
					case _: raise Exception(f"Unknown ComplexExpression: {node.type}")
			# case Node.UnaryExpression:
			# 	assert isinstance(node, Node.UnaryExpression)
			# case Node.FunctionDeclaration:
			# 	assert isinstance(node, Node.FunctionDeclaration)
			# case Node.ReturnStatement:
			# 	assert isinstance(node, Node.ReturnStatement)
			# case Node.CallExpression:
			# 	assert isinstance(node, Node.CallExpression)
			# case Node.ClassDeclaration:
			# 	assert isinstance(node, Node.ClassDeclaration)
			# case Node.Super:
			# 	assert isinstance(node, Node.Super)
			# case Node.ThisExpression:
			# 	assert isinstance(node, Node.ThisExpression)
			# case Node.NewExpression:
			# 	assert isinstance(node, Node.NewExpression)
			case Node.Literal:
				assert isinstance(node, Node.Literal)
				return node.value
			case _: raise NotImplementedError(f"{str(type(node)).split('.')[-1][:-2]} ({node.type}) is not yet implemented.")
