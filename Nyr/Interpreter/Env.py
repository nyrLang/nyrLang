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

	def findFuncOwner(self, funcName: str) -> Optional[Env]:
		if funcName in self.functions.keys(): return self
		elif self.parent is None: return None
		else: return self.parent.findFuncOwner(funcName)

	def addValue(self, varName: str, varValue):
		if self.findOwner(varName) is not None:
			raise Exception(f'Variable "{varName}" already exists in available scope')

		val = varValue
		if type(varValue) == str:
			if self.findOwner(varValue) is not None:
				val = self.getValue(varValue)
		self.update({varName: val})

	def setValue(self, varName: str, varValue):
		val = varValue
		if type(varValue) == str:
			if self.findOwner(varValue) is not None:
				val = self.getValue(varValue)
		try:
			self.findOwner(varName).update({varName: val})
		except AttributeError:
			raise Exception(f'Variable "{varName}" does not exist in available scope')

	def getValue(self, varName):
		if type(varName) != str:
			return varName
		try:
			return self.findOwner(varName).get(varName)
		except AttributeError:
			raise Exception(f'Variable "{varName}" does not exist in available scope')

	def addFunc(self, funcName: str, func: dict[str, Any]):
		# func: {"args": ["arg1", "arg2"], "body": <Node>}
		# IDEA: maybe give "func" an Env?
		if self.findFuncOwner(funcName) is not None:
			raise Exception(f'Function "{funcName}" already exists in available scope')
		self.functions.update({funcName: func})

	def getFunc(self, funcName: str):
		try:
			return self.findFuncOwner(funcName).functions.get(funcName)
		except AttributeError:
			raise Exception(f'Function "{funcName}" does not exist in available scope')
