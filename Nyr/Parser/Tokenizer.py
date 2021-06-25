import re
from typing import AnyStr
from typing import Optional

from Nyr.Parser.Node import Node

spec: list[tuple[re.Pattern[AnyStr], Optional[str]]] = [
	# -------------------------
	# Whitespace
	(re.compile(r"^\s+"), None),

	# -------------------------
	# Comments
	# Single-line
	(re.compile(r"^\/\/.*"), None),
	# Multi-line
	(re.compile(r"^\/\*[\s\S]*?\*\/.*"), None),

	# -------------------------
	# Symbols, Delimiters
	(re.compile(r"^;"), ";"),
	(re.compile(r"^\{"), "{"),
	(re.compile(r"^\}"), "}"),
	(re.compile(r"^\("), "("),
	(re.compile(r"^\)"), ")"),
	(re.compile(r"^,"), ","),

	# -------------------------
	# Keywords
	(re.compile(r"^\blet\b"), "let"),
	(re.compile(r"^\bif\b"), "if"),
	(re.compile(r"^\belse\b"), "else"),
	(re.compile(r"^\btrue\b"), "true"),
	(re.compile(r"^\bfalse\b"), "false"),
	(re.compile(r"^\bnull\b"), "null"),

	# -------------------------
	# Numbers
	(re.compile(r"^\d+\.\d+"), "FLOAT"),
	(re.compile(r"^\d+"), "INTEGER"),

	# -------------------------
	# Identifiers
	(re.compile(r"^\w+"), "IDENTIFIER"),

	# -------------------------
	# Equality Operators: ==, !=
	(re.compile(r"^[\=\!]\="), "EQUALITY_OPERATOR"),

	# -------------------------
	# Assignment Operators: =, +=, -=, *=, /=
	(re.compile(r"^\="), "SIMPLE_ASSIGN"),
	(re.compile(r"^[\+\-\*\/]\="), "COMPLEX_ASSIGN"),

	# -------------------------
	# Math Operators: +, -, *, /
	(re.compile(r"^[\+\-]"), "ADDITIVE_OPERATOR"),
	(re.compile(r"^[\*\/]"), "MULTIPLICATIVE_OPERATOR"),

	# -------------------------
	# Logical Operators: &&, ||
	(re.compile(r"^&&"), "LOGICAL_AND"),
	(re.compile(r"^\|\|"), "LOGICAL_OR"),
	(re.compile(r"^!"), "LOGICAL_NOT"),

	# -------------------------
	# Relational Operators: >, >=, <, <=
	(re.compile(r"^[><]=?"), "RELATIONAL_OPERATOR"),

	# -------------------------
	# Strings
	(re.compile(r'^"[^"]*"'), "STRING"),
	(re.compile(r"^'[^']*'"), "STRING"),
]


class Tokenizer:
	string: str = ""
	cursor: int = 0

	def __init__(self):
		pass

	def init(self, string: str):
		self.string = string
		self.cursor = 0

	def hasMoreTokens(self) -> bool: return self.cursor < len(self.string)

	def isEOF(self) -> bool: return self.cursor == len(self.string)

	def _match(self, regex: re.Pattern, string: str):
		matched = regex.match(string)

		if not matched:
			return None
		else:
			self.cursor += len(matched[0])
			return matched[0]

	def getNextToken(self) -> Optional[Node]:
		if not self.hasMoreTokens():
			return None

		string: str = self.string[self.cursor:]

		for (regex, tokenType) in spec:
			tokenValue = self._match(regex, string)

			if not tokenValue:
				continue

			if not tokenType:
				return self.getNextToken()

			node = Node()
			node.type = tokenType
			node.value = tokenValue
			return node
