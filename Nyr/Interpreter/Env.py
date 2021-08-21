from __future__ import annotations

from typing import Any
from typing import Optional


class Env(dict[str, Any]):
	parent: Env

	def __init__(self, parent=None):
		super().__init__()

		self.parent: Optional[Env] = parent
		self.functions: dict[str, dict[str, Any]] = {}

	def findOwner(self, var) -> Optional[Env]:
		if var in self: return self
		elif self.parent is None: return None
		else: return self.parent.findOwner(var)

	def addValue(self, varName: str, varValue):
		if self.findOwner(varName) is not None:
			raise Exception(f"Variable {varName} already exists")
		self.update({varName: varValue})

	def setValue(self, varName: str, varValue):
		val = varValue
		if type(varValue) == str:
			if self.findOwner(varValue) is not None:
				val = self.getValue(varValue)
		try:
			self.findOwner(varName).update({varName: val})
		except AttributeError:
			# TODO: find a way to get scope
			raise Exception(f"Variable with name {varName} does not exist in available scope")

	def getValue(self, varName):
		if type(varName) != str:
			return varName
		try:
			return self.findOwner(varName).get(varName)
		except AttributeError:
			# TODO: find a way to get scope
			raise Exception(f"Variable with name {varName} does not exist in available scope")

	def findFuncOwnder(self, funcName: str) -> Optional[Env]:
		if funcName in self.functions.keys(): return self
		elif self.parent is None: return None
		else: return self.parent.findFuncOwnder(funcName)

	def addFunc(self, funcName: str, func: dict[str, Any]):
		# func: {"args": ["arg1", "arg2"], "body": <Node>}
		# IDEA: maybe give "func" an Env?
		if self.findFuncOwnder(funcName) is not None:
			raise Exception(f"Function \"{funcName}\" already defined")
		self.functions.update({funcName: func})

	def getFunc(self, funcName: str):
		try:
			return self.findFuncOwnder(funcName).functions.get(funcName)
		except AttributeError:
			raise Exception(f"Function with name \"{funcName}\" does not exist in available scope")
