from __future__ import annotations

import re
from typing import AnyStr
from typing import Optional

from Nyr.Parser.Node import Node

spec: list[tuple[re.Pattern[AnyStr], Optional[str]]] = [
	# -------------------------
	# Whitespace
	(re.compile(r"^\n"), "NEWLINE"),
	(re.compile(r"^\s+"), None),

	# -------------------------
	# Comments
	# Single-line
	(re.compile(r"^//.*"), None),
	# Multi-line
	(re.compile(r"^/\*[\s\S]*?\*/.*"), "BLOCK_COMMENT"),

	# -------------------------
	# Symbols, Delimiters
	(re.compile(r"^;"), ";"),
	(re.compile(r"^,"), ","),
	(re.compile(r"^:"), ":"),
	(re.compile(r"^\."), "."),
	(re.compile(r"^{"), "{"),
	(re.compile(r"^}"), "}"),
	(re.compile(r"^\("), "("),
	(re.compile(r"^\)"), ")"),
	(re.compile(r"^\["), "["),
	(re.compile(r"^\]"), "]"),

	# -------------------------
	# Keywords
	(re.compile(r"^\blet\b"), "let"),
	(re.compile(r"^\bif\b"), "if"),
	(re.compile(r"^\belse\b"), "else"),
	(re.compile(r"^\btrue\b"), "true"),
	(re.compile(r"^\bfalse\b"), "false"),
	(re.compile(r"^\bnull\b"), "null"),
	(re.compile(r"^\bwhile\b"), "while"),
	(re.compile(r"^\bdo\b"), "do"),
	(re.compile(r"^\bfor\b"), "for"),
	(re.compile(r"^\bdef\b"), "def"),
	(re.compile(r"^\breturn\b"), "return"),
	(re.compile(r"^\bclass\b"), "class"),
	(re.compile(r"^\bthis\b"), "this"),
	(re.compile(r"^\bsuper\b"), "super"),
	(re.compile(r"^\bnew\b"), "new"),

	# -------------------------
	# Numbers
	(re.compile(r"^\d+\.\d+"), "FLOAT"),
	(re.compile(r"^\d+"), "INTEGER"),

	# -------------------------
	# Identifiers
	(re.compile(r"^\w+"), "IDENTIFIER"),

	# -------------------------
	# Equality Operators: ==, !=
	(re.compile(r"^[=!]="), "EQUALITY_OPERATOR"),

	# -------------------------
	# Assignment Operators: =, +=, -=, *=, /=
	(re.compile(r"^="), "SIMPLE_ASSIGN"),
	(re.compile(r"^[+\-*/%]="), "COMPLEX_ASSIGN"),

	# -------------------------
	# Math Operators: +, -, *, /
	(re.compile(r"^[+\-]"), "ADDITIVE_OPERATOR"),
	(re.compile(r"^[*/%]"), "MULTIPLICATIVE_OPERATOR"),

	# -------------------------
	# Logical Operators: &&, ||, !
	(re.compile(r"^&&"), "LOGICAL_AND"),
	(re.compile(r"^\|\|"), "LOGICAL_OR"),
	(re.compile(r"^!"), "LOGICAL_NOT"),

	# -------------------------
	# Relational Operators: >, >=, <, <=
	(re.compile(r"^[><]=?"), "RELATIONAL_OPERATOR"),

	# -------------------------
	# Strings
	(re.compile(r'^"[^"]*"'), "STRING"),
]


class Tokenizer:
	string: str = ""
	pos: Position

	def __init__(self):
		pass

	def init(self, string: str):
		self.string = string
		self.pos = Position()

	def hasMoreTokens(self) -> bool: return self.pos.cursor < len(self.string)

	def isEOF(self) -> bool: return self.pos.col == len(self.string)

	def _match(self, regex: re.Pattern, string: str):
		matched = regex.match(string)

		if not matched:
			return None
		else:
			lm = len(matched[0])
			self.pos.cursor += lm
			self.pos.col += lm
			return matched[0]

	def getNextToken(self) -> Optional[Node]:
		if not self.hasMoreTokens():
			return None

		string: str = self.string[self.pos.cursor:]

		for (regex, tokenType) in spec:
			tokenValue = self._match(regex, string)

			if not tokenValue:
				continue

			if tokenType is None:
				return self.getNextToken()
			elif tokenType == "NEWLINE":
				self.pos.line += 1
				self.pos.col = 0
				return self.getNextToken()
			elif tokenType == "BLOCK_COMMENT":
				tokenValue = tokenValue.replace(r"\\n", "_")
				self.pos.line += tokenValue.count("\n")
				self.pos.col = 0
				return self.getNextToken()

			node = Node(tokenType)
			node.value = tokenValue
			return node

		string = string.replace("\n", " ")

		raise Exception(f"Could not parse input correctly. starting here ({self.pos.line}:{self.pos.col}):\n\t{string}")


class Position:
	cursor: int
	line: int
	col: int

	def __init__(self):
		self.cursor = 0
		self.line = 1
		self.col = 0
