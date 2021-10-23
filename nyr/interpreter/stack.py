from __future__ import annotations

from enum import auto
from enum import IntEnum
from typing import Optional


class ActivationRecord:
	def __init__(self, name: str, type_: ARType, nestingLevel: int):
		self.name: str = name
		self.type: ARType = type_
		self.nestingLevel: int = nestingLevel
		self.members: dict = dict()

	def __str__(self) -> str:
		lines: list = [f"{self.nestingLevel}: {self.type} {self.name}"]

		self.cleanBuiltins()

		for key, val in self.members.items():
			if key is None: continue
			if type(val) == str:
				val = f'"{val}"'
			lines.append(f"  {key:<16} ({type(val).__name__:<6}): {val}")

		return '\n'.join(lines)

	def __repr__(self) -> str:
		self.cleanBuiltins()
		return str(self)

	def __setitem__(self, key, value):
		self.members.update({key: value})
		self.cleanBuiltins()

	def __getitem__(self, key):
		self.cleanBuiltins()
		return self.members[key]

	def cleanBuiltins(self):
		if "__builtins__" in self.members.keys():
			del self.members["__builtins__"]

	def varExists(self, varName):
		return varName in self.members.keys()

	def get(self, key):
		self.cleanBuiltins()
		return self.members.get(key, None)


class Stack(list[ActivationRecord]):
	def __str__(self) -> str:
		s = '\n'.join(repr(ar) for ar in self[::-1])
		return f"CALL STACK\n{s}\n"

	def push(self, record: ActivationRecord):
		self.append(record)

	def peek(self) -> Optional[ActivationRecord]:
		try:
			return self[-1]
		except IndexError:
			return None


class ARType(IntEnum):
	PROGRAM = auto()
	FUNCTION = auto()
