from __future__ import annotations

from enum import auto
from enum import Enum
from pprint import pp
from typing import Optional


class Stack:
	def __init__(self):
		self._records: list[ActivationRecord] = list()

	def __str__(self) -> str:
		# if "__builtins__" in self._records
		s = '\n'.join(repr(ar) for ar in self._records[::-1])
		return f"CALL STACK\n{s}\n"

	def __repr__(self) -> str:
		return str(self)

	def push(self, record: ActivationRecord):
		self._records.append(record)

	def pop(self) -> Optional[ActivationRecord]:
		return self._records.pop()

	def peek(self) -> Optional[ActivationRecord]:
		return self._records[-1]


class ARType(Enum):
	PROGRAM = auto()
	BLOCK = auto()
	FUNCTION = auto()


class ActivationRecord:
	def __init__(self, name: str, type_: ARType, nestingLevel: int):
		self.name: str = name
		self.type: ARType = type_
		self.nestingLevel: int = nestingLevel
		self.members: dict = dict()

	def __str__(self) -> str:
		lines: list = [f"{self.nestingLevel}: {self.type} {self.name}"]

		if "__builtins__" in self.members.keys():
			del self.members["__builtins__"]

		for key, val in self.members.items():
			if key is None: continue
			if type(val) == str:
				val = f'"{val}"'
			lines.append(f"  {key:<20}: {val}")

		return '\n'.join(lines)

	def __repr__(self) -> str:
		if "__builtins__" in self.members.keys():
			del self.members["__builtins__"]
		return str(self)

	def __setitem__(self, key, value):
		self.members.update({key: value})
		if "__builtins__" in self.members.keys():
			del self.members["__builtins__"]

	def __getitem__(self, key):
		if "__builtins__" in self.members.keys():
			del self.members["__builtins__"]
		return self.members[key]

	def varExists(self, varName):
		return varName in self.members.keys()

	def get(self, key):
		if "__builtins__" in self.members.keys():
			del self.members["__builtins__"]
		return self.members.get(key, None)
