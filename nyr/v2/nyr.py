#!/usr/bin/env python3
# keeping thing in one file for now, since it will be easier to self host afterwards
# because there's no support for importing files yet
from __future__ import annotations

import argparse
import logging
import math
import string as strings
import sys
from collections.abc import Generator
from collections.abc import Sequence
from enum import auto
from enum import Enum
from typing import Any
from typing import NamedTuple
from typing import Optional
from typing import Union


class _Result:
	def __init__(self, isSuccess: bool) -> None:
		self.isSuccess = isSuccess
		self.value: Union[Any, tuple[str, Any]]


class Success(_Result):
	def __init__(self, value: Any) -> None:
		super().__init__(True)
		self.value: Any = value


class Failure(_Result):
	def __init__(self, value: Union[str, Any]) -> None:
		super().__init__(False)
		self.value: Union[str, tuple[str, Any]] = value

	def __str__(self) -> str:
		if isinstance(self.value, tuple):
			errMsg: str = self.value[0]
			errToken: Any = self.value[1]
			return f"{errToken.pos.file}:{errToken.pos.line}:{errToken.pos.col}: ERROR: {errMsg}"
		else:
			return self.value


Result = Union[Success, Failure]


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
	UNDERSCORE = auto()      # discard/ignore
	PLUS = auto()            # add
	PLUS_PLUS = auto()       # increment
	PLUS_EQUAL = auto()      # add + assign
	MINUS = auto()           # subtract
	MINUS_MINUS = auto()     # decrement
	MINUS_EQUAL = auto()     # subtract + assign
	ASTERISK = auto()        # multiply
	ASTERISK_EQUAL = auto()  # multiply + assign
	SLASH = auto()           # divide
	SLASH_EQUAL = auto()     # divide + assign

	AMPERSAND = auto()            # bitwise and
	AMPERSAND_AMPERSAND = auto()  # and
	AMPERSAND_EQUAL = auto()      # bitwise and + assign
	PIPE = auto()                 # bitwise or
	PIPE_PIPE = auto()            # or
	PIPE_EQUAL = auto()           # bitwise or + assign
	BANG = auto()                 # not
	BANG_EQUAL = auto()           # not equal
	EQUAL = auto()                # assign
	EQUAL_EQUAL = auto()          # equal
	GREATER = auto()              # greater
	GREATER_EQUAL = auto()        # greater or equal
	LESSER = auto()               # lesser
	LESSER_EQUAL = auto()         # lesser or equal
	CARET = auto()                # xor
	CARET_EQUAL = auto()          # xor + assign
	PERCENT = auto()              # modulo
	PERCENT_EQUAL = auto()        # modulo + assign

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

	def __str__(self) -> str:
		return self._name_


class Position(NamedTuple):
	file: str
	line: int
	col: int

	def __str__(self) -> str:
		return f"{self.file}:{self.line}:{self.col}"

	def _message(self, tag: str, msg: str) -> None:
		print(f"{self}: {tag}: {msg}", file=sys.stderr)

	def note(self, msg: str) -> None:
		self._message("NOTE", msg)

	def error(self, msg: str) -> None:
		self._message("ERROR", msg)


class Token(NamedTuple):
	kind: TokenKind
	pos: Position
	value: Any = None

	def __str__(self) -> str:
		s = f"{str(self.pos).ljust(36)} | {str(self.kind).ljust(12)}"
		if self.value is not None:
			if self.kind == TokenKind.STRING:
				s += f' | "{self.value}"'
			else:
				s += f" | {self.value}"
		return s


logging.basicConfig(level=logging.DEBUG, format="[ %(name)s ] | %(levelname)s | %(message)s")


def tokenize(filePath: str = "stdin") -> Generator[Token, None, None]:
	with open(filePath, "r") as f:
		string = f.read()

	pos = -1
	line = 1
	col = 0

	current: Optional[str]

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

	def advance() -> Optional[str]:
		nonlocal pos
		nonlocal col
		nonlocal string

		pos += 1
		col += 1
		if pos >= len(string):
			return None
		else:
			return string[pos]

	def peek(n: int = 1) -> Optional[str]:
		nonlocal pos
		nonlocal string

		if (pos + n) >= len(string):
			return None
		else:
			return string[pos + n]

	def skip(n: int) -> None:
		if n > 0:
			for _ in range(n):
				advance()

	def makeLiteralOrKeyword(c: str, p: Position) -> Token:
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
		lit = "" + c

		while True:
			if peek() not in (strings.ascii_letters + strings.digits + "_"):
				break
			else:
				lit += advance()

		try:
			return Token(keywords[lit], p)
		except KeyError:
			return Token(TokenKind.IDENTIFIER, p, lit)

	while True:
		current = advance()
		pk = peek()

		tokenPos = Position(filePath, line, col)
		if current is None:
			yield Token(TokenKind.EOF, tokenPos)
			return
		elif current == "\n":
			line += 1
			col = 0
			continue
		elif current in (" ", "\t"):
			continue
		elif current == "+":
			try:
				yield Token(
					{
						"=": TokenKind.PLUS_EQUAL,
						"+": TokenKind.PLUS_PLUS,
					}[pk],
					tokenPos,
				)
				advance()
			except KeyError:
				yield Token(TokenKind.PLUS, tokenPos)
		elif current == "-":
			try:
				yield Token(
					{
						"=": TokenKind.MINUS_EQUAL,
						"-": TokenKind.MINUS_MINUS,
					}[pk],
					tokenPos,
				)
				advance()
			except KeyError:
				yield Token(TokenKind.MINUS, tokenPos)
		elif current == "*":
			if pk == "=":
				yield Token(TokenKind.ASTERISK_EQUAL, tokenPos)
				advance()
			else:
				yield Token(TokenKind.ASTERISK, tokenPos)
		elif current == "/":
			if pk == "=":
				yield Token(TokenKind.SLASH_EQUAL, tokenPos)
				advance()
			elif pk == "/":
				# single-line comment
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
				# multi-line comment
				advance()
				while True:
					current = advance()
					if current is None:
						tokenPos.error("unclosed multiline comment")
						return
					elif current == "*" and peek() == "/":
						advance()
						break
					elif current == "\n":
						line += 1
						col = 0
			else:
				yield Token(TokenKind.SLASH, tokenPos)
		elif current == "%":
			if pk == "=":
				yield Token(TokenKind.PERCENT_EQUAL, tokenPos)
				advance()
			else:
				yield Token(TokenKind.PERCENT, tokenPos)
		elif current == "&":
			try:
				yield Token(
					{
						"&": TokenKind.AMPERSAND_AMPERSAND,
						"=": TokenKind.AMPERSAND_EQUAL,
					}[pk],
					tokenPos,
				)
				advance()
			except KeyError:
				yield Token(TokenKind.AMPERSAND, tokenPos)
		elif current == "|":
			try:
				yield Token(
					{
						"|": TokenKind.PIPE_PIPE,
						"=": TokenKind.PIPE_EQUAL,
					}[pk],
					tokenPos,
				)
				advance()
			except KeyError:
				yield Token(TokenKind.PIPE, tokenPos)
		elif current == "!":
			if pk == "=":
				yield Token(TokenKind.BANG_EQUAL, tokenPos)
				advance()
			else:
				yield Token(TokenKind.BANG, tokenPos)
		elif current == "=":
			if pk == "=":
				yield Token(TokenKind.EQUAL_EQUAL, tokenPos)
				advance()
			else:
				yield Token(TokenKind.EQUAL, tokenPos)
		elif current == ">":
			if pk == "=":
				yield Token(TokenKind.GREATER_EQUAL, tokenPos)
				advance()
			else:
				yield Token(TokenKind.GREATER, tokenPos)
		elif current == "<":
			if pk == "=":
				yield Token(TokenKind.LESSER_EQUAL, tokenPos)
				advance()
			else:
				yield Token(TokenKind.LESSER, tokenPos)
		elif current == "^":
			if pk == "=":
				yield Token(TokenKind.CARET_EQUAL, tokenPos)
				advance()
			else:
				yield Token(TokenKind.CARET, tokenPos)
		elif current == '"':
			literal = ""

			while True:
				char = peek()

				if char == '"':
					# skip ending double quote
					advance()
					break
				elif char == "\n":
					line += 1
					col = 0
				elif char == "\\":
					# check if quote is escaped
					escapes = 1
					while True:
						char = peek(escapes + 1)
						if char != "\\":
							break
						escapes += 1

					skip(escapes)
					# counted backslashes
					if peek() == '"':
						literal += "\\" * (escapes // 2)
						# check if quote is escaped
						if escapes % 2 == 0:
							advance()
							break
					else:
						# just escaped backslashes
						literal += "\\" * math.ceil(escapes / 2)

				s = advance()
				if s is None:
					tokenPos.error("unlosed string")
					return
				else:
					literal += s

			yield Token(TokenKind.STRING, tokenPos, literal)
		elif current == '_':
			if pk in (strings.digits + strings.ascii_letters + "_"):
				yield makeLiteralOrKeyword(current, tokenPos)
			else:
				yield Token(TokenKind.UNDERSCORE, tokenPos)
		elif current in simpleTokens.keys():
			yield Token(simpleTokens[current], tokenPos)
		elif current in strings.digits:
			numStr = "" + current
			dotCount = 0

			while True:
				char = peek()
				if char == ".":
					dotCount += 1
					if dotCount > 1:
						tokenPos.error("number contains multiple dots (`.`)")
						break
					numStr += advance()

				if char not in (strings.digits + "."):
					break

				numStr += advance()

			try:
				_k, _f = {
					0: (TokenKind.INTEGER, int),
					1: (TokenKind.FLOAT, float),
				}[dotCount]
				yield Token(_k, tokenPos, _f(numStr))
			except KeyError:
				continue
		elif current in strings.ascii_letters:
			yield makeLiteralOrKeyword(current, tokenPos)
		else:
			unknown = "" + current
			while True:
				if peek() in (" ", "\t", "\n", None):
					break

				unknown += advance()

			tokenPos.error(f"Unknown sequence of characters: `{unknown}`")


def _checkToken(tokens: Sequence[Token], idx: int, token: Token) -> tuple[bool, int]:
	success = True
	i = idx

	def err(msg: str) -> None:
		nonlocal i
		nonlocal tokens
		print(f"{tokens[i].pos}: ERROR: {msg}", file=sys.stderr)

	if token.kind == TokenKind.LET:
		# maybe only check until end of line?
		# but that would break defining them over multiple lines
		# if you wanted do do that (for whatever reason)
		while tokens[i].kind != TokenKind.SEMICOLON and i < len(tokens):
			i += 1
			# Check variable name is identifier
			varName = tokens[i]
			sccss = True
			if varName.kind != TokenKind.IDENTIFIER:
				err(f"Expected variable name, got {varName.kind}")
				success = False
				i += 1
				if tokens[i].kind == TokenKind.SEMICOLON:
					i += 1
					break
				elif tokens[i].kind == TokenKind.EQUAL:
					i += 1
					if tokens[i].kind not in (TokenKind.NULL, TokenKind.TRUE, TokenKind.FALSE, TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.STRING):
						err(
							f"expected one of: "
							f"{', '.join(str(k) for k in (TokenKind.NULL, TokenKind.TRUE, TokenKind.FALSE, TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.STRING))}; "
							f"got {tokens[i].kind}",
						)
						sccss = False
					else:
						i += 1
						continue
				elif tokens[i].kind == TokenKind.COMMA:
					i += 1
					continue
				else:
					err(
						f"expected one of: "
						f"{', '.join(str(k) for k in (TokenKind.SEMICOLON, TokenKind.EQUAL, TokenKind.COMMA))}; "
						f"got {tokens[i + 1].kind}",
					)
					i += 1
					continue

			if sccss is False or success is False:
				return (False, i - idx)

			i += 1
			# Check variable value (if it exists)
			if tokens[i].kind == TokenKind.SEMICOLON:
				# no value and end of declarations
				break
			elif tokens[i].kind == TokenKind.COMMA:
				# no value but more declarations
				continue
			elif tokens[i].kind == TokenKind.EQUAL:
				# expect value
				i += 1
				if tokens[i].kind not in (
					TokenKind.NULL,
					TokenKind.TRUE, TokenKind.FALSE,
					TokenKind.INTEGER, TokenKind.FLOAT,
					TokenKind.STRING,
					TokenKind.IDENTIFIER,
				):
					err(
						f"expected one of: "
						f"{', '.join(str(k) for k in (TokenKind.NULL, TokenKind.TRUE, TokenKind.FALSE, TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.STRING, TokenKind.IDENTIFIER))}; "
						f"got {tokens[i].kind}",
					)
					success = False
				else:
					i += 1
					continue
			else:
				err(
					f"expected one of: "
					f"{', '.join(str(k) for k in (TokenKind.SEMICOLON, TokenKind.COMMA, TokenKind.EQUAL))}; "
					f"got {tokens[i].kind}",
				)
				success = False
				continue

		if i == len(tokens):
			err("expected semicolon after variable declaration(s)")
			success = False
	elif token.kind == TokenKind.EOF:
		if idx + 1 != len(tokens):
			err("found more tokens after EOF")
			success = False
	else:
		err(f"checking {token.kind} is not implemented")
		success = False

	return (success, i - idx)


def checkTokens(tokenStream: Sequence[Token]) -> bool:
	checkPassed = True

	skipN = 0
	for i, token in enumerate(tokenStream):
		if skipN > 0:
			skipN -= 1
			continue

		try:
			passed, n = _checkToken(tokenStream, i, token)
		except IndexError:
			print(f"{token.pos}: ERROR: unexepected end of input", file=sys.stderr)
			return False

		if n < 0:
			n = 0

		skipN += n
		checkPassed &= passed

	return checkPassed


def main(args: Sequence[str] = None) -> int:
	assert sys.version_info >= (3, 9), "At lest python 3.9 is required"

	argParser = argparse.ArgumentParser()
	argParser.add_argument("file", help="input file to interpret/compile")
	# not sure on how to implement debug mode yet
	argParser.add_argument(
		"-d", "--debug",
		action="store_true",
		dest="debug",
		help="enable debug mode (not implemented)",
	)
	argParser.add_argument(
		"-c", "--compile",
		action="store_true",
		dest="compile",
		help="compile file instead of interpreting it (not implemented)",
	)
	# somewhat clashes with how checkTokens is implemented
	argParser.add_argument(
		"-u", "--unsafe",
		action="store_true",
		dest="unsafe",
		help="disable type checking code (not implemented; currently always skipped)",
	)

	parsedArgs = argParser.parse_args(args)

	if parsedArgs.debug is True:
		print("debug mode is not implemented")
	if parsedArgs.compile is True:
		print("compile mode is not implemented")
	if parsedArgs.unsafe is True:
		print("unsafe mode is not implemented")

	tokens: list[Token] = [token for token in tokenize(parsedArgs.file)]

	# for token in tokens:
	# 	print(token)

	checkPassed = checkTokens(tokens)
	print("checks " + ("passed" if checkPassed else "failed"))

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
