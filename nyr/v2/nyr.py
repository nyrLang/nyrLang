#!/usr/bin/env python3
# keeping this in one file for now, since it will be easier to self host afterwards
# because there's no support for importing files yet
from __future__ import annotations

import argparse
import importlib.metadata
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


logging.basicConfig(level=logging.DEBUG, format="[ %(name)s ] | %(levelname)s | %(message)s")


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
	UNDERSCORE = auto()
	OPERATOR = auto()
	BACKTICK = auto()
	PLUS = auto()
	MINUS = auto()
	ASTERISK = auto()
	SLASH = auto()

	AMPERSAND = auto()
	PIPE = auto()
	BANG = auto()
	EQUAL = auto()
	GREATER = auto()
	LESSER = auto()
	CARET = auto()
	PERCENT = auto()

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

	@staticmethod
	def _kindToOperatorStr() -> dict[TokenKind, str]:
		return {
			TokenKind.PLUS: "+",
			TokenKind.MINUS: "-",
			TokenKind.ASTERISK: "*",
			TokenKind.SLASH: "/",
			TokenKind.PERCENT: "%",
			TokenKind.BANG: "!",
			TokenKind.AMPERSAND: "&",
			TokenKind.PIPE: "|",
			TokenKind.CARET: "^",
			TokenKind.EQUAL: "=",
			TokenKind.LESSER: "<",
			TokenKind.GREATER: ">",
		}

	@staticmethod
	def _operatorStrToKind() -> dict[str, TokenKind]:
		return {v: k for (k, v) in TokenKind._kindToOperatorStr().items()}

	@staticmethod
	def stringToOperator(op: str) -> TokenKind:
		return TokenKind._operatorStrToKind()[op]

	@staticmethod
	def stringifyOperator(op: TokenKind) -> str:
		return TokenKind._kindToOperatorStr()[op]


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
			elif self.kind == TokenKind.OPERATOR:
				assert isinstance(self.value, tuple)
				s += f" | {''.join(TokenKind.stringifyOperator(_op) for _op in self.value)}"
			else:
				s += f" | {self.value}"
		return s


def tokenize(filePath: str) -> Generator[Token, bool]:
	with open(filePath, "r") as f:
		string = f.read()

	pos = -1
	line = 1
	col = 0

	success = True

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
		"`": TokenKind.BACKTICK,
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
			return success
		elif current == "\n":
			line += 1
			col = 0
			continue
		elif current in (" ", "\t"):
			continue
		# special handling for single-/multi-line comments
		elif current == "/" and peek() == "/":
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
		elif current == "/" and peek() == "*":
			# multi-line comment
			advance()
			while True:
				current = advance()
				if current is None:
					tokenPos.error("unclosed multiline comment")
					return False
				elif current == "*" and peek() == "/":
					advance()
					break
				elif current == "\n":
					line += 1
					col = 0
		elif current in TokenKind._operatorStrToKind().keys():
			# dynamically generate operators
			ops: list[TokenKind] = []

			while current in TokenKind._operatorStrToKind().keys():
				ops.append(TokenKind.stringToOperator(current))
				current = advance()

			yield Token(TokenKind.OPERATOR, tokenPos, tuple(ops))
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
					return False
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
						success = False
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
			except KeyError:
				continue
			else:
				yield Token(_k, tokenPos, _f(numStr))
		elif current in strings.ascii_letters:
			yield makeLiteralOrKeyword(current, tokenPos)
		else:
			unknown = "" + current
			while True:
				if peek() in (" ", "\t", "\n", None):
					break

				unknown += advance()

			tokenPos.error(f"Unknown sequence of characters: `{unknown}`")
			success = False


def _checkToken(tokens: Sequence[Token], idx: int) -> tuple[bool, int]:
	success = True
	i = idx
	token = tokens[idx]

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
				varName.pos.error(f"Expected variable name, got {varName.kind}")
				success = False
				i += 1
				if tokens[i].kind == TokenKind.SEMICOLON:
					i += 1
					break
				elif tokens[i].kind == TokenKind.EQUAL:
					i += 1
					if tokens[i].kind not in (TokenKind.NULL, TokenKind.TRUE, TokenKind.FALSE, TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.STRING):
						tokens[i].pos.error(
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
					i += 1
					tokens[i].pos.error(
						f"expected one of: "
						f"{', '.join(str(k) for k in (TokenKind.SEMICOLON, TokenKind.EQUAL, TokenKind.COMMA))}; "
						f"got {tokens[i].kind}",
					)
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
			elif tokens[i].kind == TokenKind.OPERATOR:
				# expect `=`
				t = tokens[i]
				assert isinstance(t.value, tuple)

				if t.value != (TokenKind.EQUAL,):
					_op = ""
					success = False
					for _t in t.value:
						assert isinstance(_t, TokenKind)
						_op += TokenKind.stringifyOperator(_t)
					if len(_op) == 0:
						tokens[i].pos.error("expected `=`, got nothing")
					else:
						tokens[i].pos.error(f"expected `=`, got {_op}")
					del _op
				# still continue normally even if operator is wrong, to catch more errors

				# expect value
				i += 1
				if tokens[i].kind not in (
					TokenKind.NULL,
					TokenKind.TRUE, TokenKind.FALSE,
					TokenKind.INTEGER, TokenKind.FLOAT,
					TokenKind.STRING,
					TokenKind.IDENTIFIER,
				):
					tokens[i].pos.error(
						f"expected one of: "
						f"{', '.join(str(k) for k in (TokenKind.NULL, TokenKind.TRUE, TokenKind.FALSE, TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.STRING, TokenKind.IDENTIFIER))}; "
						f"got {tokens[i].kind}",
					)
					success = False
				else:
					i += 1
					continue
			else:
				tokens[i].pos.error(
					f"expected one of: "
					f"{', '.join(str(k) for k in (TokenKind.SEMICOLON, TokenKind.COMMA, TokenKind.EQUAL))}; "
					f"got {tokens[i].kind}",
				)
				success = False
				continue

		if i == len(tokens):
			tokens[i].pos.error("expected semicolon after variable declaration(s)")
			success = False
	elif token.kind == TokenKind.EOF:
		if idx + 1 != len(tokens):
			tokens[i].pos.error("found more tokens after EOF")
			success = False
	else:
		tokens[i].pos.error(f"checking {token.kind} is not implemented")
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
			passed, n = _checkToken(tokenStream, i)
		except IndexError:
			token.pos.error("unexpected end of input")
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
		"-c", "--compiler",
		default="default",
		dest="compiler",
		help="choose a compiler (or interpreter) (badly implemented)",
	)
	# somewhat clashes with how checkTokens is implemented
	argParser.add_argument(
		"-u", "--unsafe",
		action="store_true",  # TODO: change to "store_false" when checking is implemented
		dest="unsafe",
		help="disable checking code (very likely breaks things; currently always on, since checking is pretty much not implemented; can be turned off by using this flag)",
	)

	parsedArgs = argParser.parse_args(args)

	if parsedArgs.debug is True:
		print("debug mode is not (fully) implemented")

	tokens: list[Token] = []
	tks = tokenize(parsedArgs.file)

	while True:
		try:
			tokens.append(next(tks))
		except StopIteration as stop:
			if stop.value is False:
				print(f"{parsedArgs.file}: ERROR: tokenization failed", file=sys.stderr)
				return 1
			else:
				break

	if parsedArgs.debug is True:
		print("\n".join(str(token) for token in tokens))

	if parsedArgs.unsafe is False:
		if checkTokens(tokens) is False:
			print(f"{parsedArgs.file}: ERROR: checks failed", file=sys.stderr)
			return 1

	compilers = {
		entrypoint.name: entrypoint
		for entrypoint in importlib.metadata.entry_points()["nyr.compiler"]
	}

	try:
		compiler = compilers[parsedArgs.compiler].load()
	except KeyError:
		print(
			f"compiler {parsedArgs.compiler} does not exist\n"
			f"available compilers: {', '.join(sorted(compilers))}",
			file=sys.stderr,
		)
		return 1
	else:
		compiler(tokens)

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
