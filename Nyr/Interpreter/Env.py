from pprint import pprint
from typing import Any


class Env(dict):
	def __init__(self, parent=None):
		super().__init__()

		self.parent: Env = parent

	def find(self, var):
		if var in self: return self
		elif self.parent is None: return None
		else: return self.parent.find(var)

	def addChildEnv(self, name: str, env):
		c = self.find(name)
		if c is None:
			self[name] = env
		elif c == self:
			raise Exception(f"'{name}' already exisis in current scope")
		else:
			raise Exception(f"'{name}' shadows '{name}' from outer scope")

	def addVar(self, name, value):
		var = self.find(name)
		if var is None:
			self[name] = value
		elif var == self:
			raise Exception(f"Variable '{name}' already exisis in current scope")
		else:
			raise Exception(f"Variable '{name}' shadows variable from outer scope")

	def getVar(self, name):
		var = self.find(name)
		if var is None:
			raise Exception(f"Variable '{name}' does not exist in current or outer scope")
		else:
			return var[name]

	def setVar(self, name, value):
		var = self.find(name)
		if var is None:
			raise Exception(f"Variable '{name}' does not exist in current or outer scope")
		else:
			self.find(name)[name] = value

	def addFunc(self, name, parameters, body):
		f = self.find(name)
		if f is None:
			func: dict[str, Any] = {
				"__name_": name,
				"__body_": body,
			}
			for param in parameters: func[param] = None
			self[f"__f_{name}"] = func
		elif f is self:
			raise Exception(f"Function '{name}' already exists in current scope")
		else:
			raise Exception(f"Function '{name}' shadows function from outer scope")

	def getFunc(self, name):
		func = self.find(name)
		if func is None:
			raise Exception(f"Function '{name}' does not exist in current or outer scope")
		else:
			return func[name]
