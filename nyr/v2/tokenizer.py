from __future__ import annotations

import logging
import string as strings
from enum import Enum
from enum import auto
from typing import Any
from typing import NamedTuple
from typing import Sequence
from typing import Union


class _Result:
	def __init__(self, isSuccess: bool) -> None:
		self.isSuccess = isSuccess
		self.value: Union[Token, tuple[str, Token]]


class Success(_Result):
	def __init__(self, value: Token) -> None:
		super().__init__(True)
		self.value: Token = value


class Failure(_Result):
	def __init__(self, value: tuple[str, Token]) -> None:
		super().__init__(False)
		self.value: tuple[str, Token] = value

	def __str__(self) -> str:
		errMsg: str = self.value[0]
		errToken: Token = self.value[1]
		return f"{errToken.file}:{errToken.pos.line}:{errToken.pos.col}: {errMsg}"


Result = Union[Success, Failure]


class TokenPos(NamedTuple):
	line: int
	col: int


class TokenKind(Enum):
	LPAREN = auto()
	RPAREN = auto()
	LBRACE = auto()
	RBRACE = auto()
	LBRACKET = auto()
	RBRACKET = auto()
	DOT = auto()
	COLON = auto()
	COMMA = auto()
	SEMICOLON = auto()
	PLUS = auto()
	PLUS_PLUS = auto()
	PLUS_EQUAL = auto()
	MINUS = auto()
	MINUS_MINUS = auto()
	MINUS_EQUAL = auto()
	ASTERISK = auto()
	ASTERISK_EQUAL = auto()
	SLASH = auto()
	SLASH_EQUAL = auto()

	AMPERSAND = auto()
	AMPERSAND_AMPERSAND = auto()
	PIPE = auto()
	PIPE_PIPE = auto()
	BANG = auto()
	BANG_EQUAL = auto()
	EQUAL = auto()
	EQUAL_EQUAL = auto()
	GREATER = auto()
	GREATER_EQUAL = auto()
	LESSER = auto()
	LESSER_EQUAL = auto()
	CARET = auto()
	CARET_EQUAL = auto()

	# Literals
	IDENTIFIER = auto()
	STRING = auto()
	INTEGER = auto()
	FLOAT = auto()

	# Keywords
	LET = auto()
	IF = auto()
	ELSE = auto()
	TRUE = auto()
	FALSE = auto()
	NULL = auto()
	WHILE = auto()
	DO = auto()
	FOR = auto()
	DEF = auto()
	RETURN = auto()
	CLASS = auto()
	THIS = auto()
	SUPER = auto()

	# Builtins
	PRINT = auto()

	EOF = auto()


class Token(NamedTuple):
	kind: TokenKind
	pos: TokenPos
	file: str
	value: Any = None


logging.basicConfig(
	level=logging.DEBUG,
	filename="debug/logFile.txt",
	filemode="w",
	format="[ %(name)s ] | %(levelname)s | %(message)s",
)


def tokenize(string: str, filePath: str = "stdin") -> Sequence[Result]:
	# absolute position in string
	pos = -1

	# relative positions for tokens
	line = 1
	col = 0

	current: Union[str, None]

	def advance() -> str:
		nonlocal pos
		nonlocal col
		nonlocal string

		pos += 1
		col += 1
		if pos >= len(string):
			return None
		else:
			return string[pos]

	def peek(n: int = 1) -> Union[str, None]:
		nonlocal pos
		nonlocal string

		if (pos + n) >= len(string):
			return None
		else:
			return string[pos + n]

	simpleTokens = {
		"(": TokenKind.LPAREN,
		")": TokenKind.RPAREN,
		"{": TokenKind.LBRACE,
		"}": TokenKind.RBRACE,
		"[": TokenKind.LBRACKET,
		"]": TokenKind.RBRACKET,
		".": TokenKind.DOT,
		",": TokenKind.COMMA,
		":": TokenKind.COLON,
		";": TokenKind.SEMICOLON,
	}
	keywords = {
		"let": TokenKind.LET,
		"if": TokenKind.IF,
		"else": TokenKind.ELSE,
		"true": TokenKind.TRUE,
		"false": TokenKind.FALSE,
		"null": TokenKind.NULL,
		"while": TokenKind.WHILE,
		"do": TokenKind.DO,
		"for": TokenKind.FOR,
		"def": TokenKind.DEF,
		"return": TokenKind.RETURN,
		"class": TokenKind.CLASS,
		"this": TokenKind.THIS,
		"super": TokenKind.SUPER,
		"print": TokenKind.PRINT,
	}

	while True:
		current = advance()

		if current is None:
			yield Success(Token(TokenKind.EOF, TokenPos(line, col), filePath))
			return
		elif current in ("\n", "\r\n"):
			line += 1
			col = 0
			continue
		elif current in (" ", "\t"):
			continue
		elif current == "+":
			pk = peek()
			if pk == "=":
				yield Success(Token(TokenKind.PLUS_EQUAL, TokenPos(line, col), filePath))
				advance()
			elif pk == "+":
				yield Success(Token(TokenKind.PLUS_PLUS, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.PLUS, TokenPos(line, col), filePath))
		elif current == "-":
			pk = peek()
			if pk == "=":
				yield Success(Token(TokenKind.MINUS_EQUAL, TokenPos(line, col), filePath))
				advance()
			elif pk == "-":
				yield Success(Token(TokenKind.MINUS_MINUS, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.MINUS, TokenPos(line, col), filePath))
		elif current == "*":
			pk = peek()
			if pk == "=":
				yield Success(Token(TokenKind.ASTERISK_EQUAL, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.ASTERISK, TokenPos(line, col), filePath))
		elif current == "/":
			pk = peek()
			if pk == "/":
				# Single-line comment
				advance()
				while True:
					current = advance()
					if current == "\n":
						line += 1
						col = 0
						break
					elif current is None:
						break
			elif pk == "*":
				# Multi-line comment
				advance()
				while True:
					current = advance()
					if current == "*" and peek() == "/":
						advance()
						break
					elif current == "\n":
						line += 1
						col = 0
			elif pk == "=":
				yield Success(Token(TokenKind.SLASH_EQUAL, TokenPos(line, col), filePath))
			else:
				yield Success(Token(TokenKind.SLASH, TokenPos(line, col), filePath))
		elif current == "&":
			pk = peek()
			if pk == "&":
				yield Success(Token(TokenKind.AMPERSAND_AMPERSAND, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.AMPERSAND, TokenPos(line, col), filePath))
		elif current == "|":
			pk = peek()
			if pk == "|":
				yield Success(Token(TokenKind.PIPE_PIPE, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.PIPE, TokenPos(line, col), filePath))
		elif current == "!":
			pk = peek()
			if pk == "=":
				yield Success(Token(TokenKind.BANG_EQUAL, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.BANG, TokenPos(line, col), filePath))
		elif current == "=":
			pk = peek()
			if pk == "=":
				yield Success(Token(TokenKind.EQUAL_EQUAL, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.EQUAL, TokenPos(line, col), filePath))
		elif current == ">":
			pk = peek()
			if pk == "=":
				yield Success(Token(TokenKind.GREATER_EQUAL, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.GREATER, TokenPos(line, col), filePath))
		elif current == "<":
			pk = peek()
			if pk == "=":
				yield Success(Token(TokenKind.LESSER_EQUAL, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.LESSER, TokenPos(line, col), filePath))
		elif current == "^":
			pk = peek()
			if pk == "=":
				yield Success(Token(TokenKind.CARET_EQUAL, TokenPos(line, col), filePath))
				advance()
			else:
				yield Success(Token(TokenKind.CARET, TokenPos(line, col), filePath))
		elif current in simpleTokens.keys():
			yield Success(Token(simpleTokens[current], TokenPos(line, col), filePath))
		elif current in strings.digits:
			numstr = "" + current
			dotCount = 0

			startLine = line
			startCol = col

			while True:
				char = peek()

				if char == ".":
					dotCount += 1
					if dotCount > 1:
						yield Failure(f"{filePath}:{line}:{col}: number contains multiple dots (`.`)")
						break
					numstr += advance()

				if char not in (strings.digits + "."):
					break

				numstr += advance()

			if dotCount == 0:
				yield Success(Token(TokenKind.INTEGER, TokenPos(startLine, startCol), filePath, int(numstr)))
			elif dotCount == 1:
				yield Success(Token(TokenKind.FLOAT, TokenPos(startLine, startCol), filePath, float(numstr)))
			else:
				continue
		elif current in strings.ascii_letters:
			idStr = "" + current

			startLine = line
			startCol = col

			while True:
				char = peek()

				if char not in (strings.ascii_letters + strings.digits + "_"):
					break

				idStr += advance()

			if idStr in keywords.keys():
				yield Success(Token(keywords[idStr], TokenPos(startLine, startCol), filePath))
			else:
				yield Success(Token(TokenKind.IDENTIFIER, TokenPos(startLine, startCol), filePath, idStr))
		else:
			yield Failure(f"{filePath}:{line}:{col}: Unknown character: {current}")
