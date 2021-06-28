class Env(dict):
	def __init__(self, parent=None):
		super().__init__()

		self.parent: Env = parent

	def find(self, var):
		return self if var in self else self.parent.find(var)

	def addChild(self, name: str, env):
		self[name] = env
