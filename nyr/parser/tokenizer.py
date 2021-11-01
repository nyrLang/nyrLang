from __future__ import annotations

import re
from collections.abc import Iterable
from typing import NamedTuple
from typing import Optional
from typing import Union

spec: tuple[tuple[re.Pattern[str], Optional[str]], ...] = (
	# -------------------------
	# Whitespace
	(re.compile(r"\n"), "NEWLINE"),
	(re.compile(r"\s+"), None),

	# -------------------------
	# Comments
	# Single-line
	(re.compile(r"//.*"), None),
	# Multi-line
	(re.compile(r"/\*[\s\S]*?\*/.*"), "BLOCK_COMMENT"),

	# -------------------------
	# Symbols, Delimiters
	(re.compile(r";"), ";"),
	(re.compile(r","), ","),
	(re.compile(r":"), ":"),
	(re.compile(r"\."), "."),
	(re.compile(r"{"), "{"),
	(re.compile(r"}"), "}"),
	(re.compile(r"\("), "("),
	(re.compile(r"\)"), ")"),
	(re.compile(r"\["), "["),
	(re.compile(r"\]"), "]"),

	# -------------------------
	# Keywords
	(re.compile(r"\blet\b"), "let"),
	(re.compile(r"\bif\b"), "if"),
	(re.compile(r"\belse\b"), "else"),
	(re.compile(r"\btrue\b"), "true"),
	(re.compile(r"\bfalse\b"), "false"),
	(re.compile(r"\bnull\b"), "null"),
	(re.compile(r"\bwhile\b"), "while"),
	(re.compile(r"\bdo\b"), "do"),
	(re.compile(r"\bfor\b"), "for"),
	(re.compile(r"\bdef\b"), "def"),
	(re.compile(r"\breturn\b"), "return"),
	(re.compile(r"\bclass\b"), "class"),
	(re.compile(r"\bthis\b"), "this"),
	(re.compile(r"\bsuper\b"), "super"),

	# -------------------------
	# Numbers
	(re.compile(r"\d+\.\d+"), "FLOAT"),
	(re.compile(r"\d+"), "INTEGER"),

	# -------------------------
	# Identifiers
	(re.compile(r"\w+"), "IDENTIFIER"),

	# -------------------------
	# Equality Operators: ==, !=
	(re.compile(r"[=!]="), "EQUALITY_OPERATOR"),

	# -------------------------
	# Assignment Operators: =, +=, -=, *=, /=
	(re.compile(r"="), "SIMPLE_ASSIGN"),
	(re.compile(r"[+\-*/%]="), "COMPLEX_ASSIGN"),

	# -------------------------
	# Math Operators: +, -, *, /
	(re.compile(r"[+\-]"), "ADDITIVE_OPERATOR"),
	(re.compile(r"[*/%]"), "MULTIPLICATIVE_OPERATOR"),

	# -------------------------
	# Logical Operators: &&, ||, !
	(re.compile(r"&&"), "LOGICAL_AND"),
	(re.compile(r"\|\|"), "LOGICAL_OR"),
	(re.compile(r"!"), "LOGICAL_NOT"),

	# -------------------------
	# Bitwise Operators
	(re.compile(r"\&"), "BITWISE_AND"),
	(re.compile(r"\^"), "BITWISE_XOR"),
	(re.compile(r"\|"), "BITWISE_OR"),

	# -------------------------
	# Relational Operators: >, >=, <, <=
	(re.compile(r"[><]=?"), "RELATIONAL_OPERATOR"),

	# -------------------------
	# Strings
	(re.compile(r'"[^"]*"'), "STRING"),
)


class Token(NamedTuple):
	type: str
	value: Union[None, int, float, bool, str]

	def __str__(self) -> str:
		return f"{self.type:<12} | {self.value:<16}"

	def __repr__(self):
		return f"{self.__module__}.{self.__class__.__name__}({self.type!r}{f', {self.value}' if self.value is not None else ''})"


class Tokenizer:
	def __init__(self) -> None:
		self.string = ""
		self.pos: Position

	def _advance(self, cursor: int = 1, col: int = 1) -> None:
		self.pos.cursor += cursor
		self.pos.col += col

	def _newLine(self) -> None:
		self.pos.cursor += 1
		self.pos.col = 0
		self.pos.line += 1

	def _reset(self):
		self.string = ""
		self.pos = Position()

	def init(self, string: str):
		self._reset()
		self.string = string

	def hasMoreTokens(self) -> bool:
		return self.pos.cursor < len(self.string)

	def _match(self, regex: re.Pattern):
		matched = regex.match(self.string, self.pos.cursor)

		if not matched:
			return None
		else:
			lm = len(matched[0])
			self._advance(lm, lm)
			return matched[0]

	def _getNextToken(self) -> Token:
		if not self.hasMoreTokens():
			return Token("EOF", None)

		for (regex, tokenType) in spec:
			tokenValue = self._match(regex)

			if not tokenValue:
				continue

			if tokenType is None:
				pass
			elif tokenType == "NEWLINE":
				self._newLine()
			elif tokenType == "BLOCK_COMMENT":
				self.pos.line += tokenValue.count("\n")
				self.pos.col = 0
			else:
				return Token(tokenType, tokenValue)

			return self._getNextToken()

		string = self.string[self.pos.cursor:].replace("\n", " ")

		raise SyntaxError(f"Could not parse input correctly. starting here ({self.pos.line}:{self.pos.col}):\n  {string}")

	def tokenize(self, string: str) -> Iterable[Token]:
		tk = self._getNextToken()
		while tk.type != "EOF":
			yield tk
			tk = self._getNextToken()
		yield tk

	def getTokens(self) -> tuple[Token, ...]:
		tokens = []
		tk = self._getNextToken()
		while tk.type != "EOF":
			tokens.append(tk)
			tk = self._getNextToken()
		tokens.append(tk)
		return tuple(tokens)


class Position:
	def __init__(self):
		self.cursor = 0
		self.line = 1
		self.col = 0

	def __str__(self) -> str:
		return f"{self.line}:{self.col}"
