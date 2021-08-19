from __future__ import annotations

from typing import Any
from typing import Optional


class Env(dict[str, Any]):
	parent: Env

	def __init__(self, parent=None):
		super().__init__()

		self.parent: Optional[Env] = parent

	def findOwner(self, var) -> Optional[Env]:
		if var in self: return self
		elif self.parent is None: return None
		else: return self.parent.findOwner(var)
