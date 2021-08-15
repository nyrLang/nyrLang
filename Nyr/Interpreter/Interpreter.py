from typing import Any

from Nyr.Interpreter.Env import Env
from Nyr.Parser import Node


class Interpreter:
	def interpret(self, node: Node.Node, env: Env) -> Any:
		if node is None: return None

		raise NotImplementedError(f"{node.type} is not yet implemented.")
