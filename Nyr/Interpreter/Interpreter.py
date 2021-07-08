from typing import Any

from Nyr.Interpreter.Env import Env
from Nyr.Parser import Node


class Interpreter:
	def interpret(self, node: Node.Node, env: Env) -> Any:
		if node is None: return None

		match type(node):
			# case Node.Program:
			# case Node.VariableDeclaration:
			# case Node.Identifier:
			# case Node.ExpressionStatement:
			# case Node.EmptyStatement:
			# case Node.BlockStatement:
			# case Node.IfStatement:
			# case Node.VariableStatement:
			# case Node.WhileStatement:
			# case Node.ForStatement:
			# case Node.ComplexExpression:
			# case Node.UnaryExpression:
			# case Node.FunctionDeclaration:
			# case Node.ReturnStatement:
			# case Node.CallExpression:
			# case Node.ClassDeclaration:
			# case Node.Super:
			# case Node.ThisExpression:
			# case Node.NewExpression:
			# case Node.Literal:
			case _: raise NotImplementedError(f"{node.type} is not yet implemented.")
