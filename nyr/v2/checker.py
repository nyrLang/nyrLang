from typing import Sequence

from nyr.v2.tokenizer import Failure
from nyr.v2.tokenizer import Result
from nyr.v2.tokenizer import Success
from nyr.v2.tokenizer import Token
from nyr.v2.tokenizer import TokenKind


def checkTokens(tokenStream: Sequence[Result]) -> tuple[Sequence[Token], bool]:
	"""
		check tokens for syntax and logic errors
		such as divide by 0 and missing semicolons
	"""

	checkPassed = True
	tks: Sequence[Token] = []

	for tokenResult in tokenStream:
		if tokenResult.isSuccess is False:
			checkPassed = False
			assert isinstance(tokenResult, Failure)
			print(tokenResult)
			tks.append(tokenResult.value[1])
		else:
			assert isinstance(tokenResult, Success)
			tks.append(tokenResult.value)

	if checkPassed is True:
		skipN = 0
		for i, token in enumerate(tks):
			if skipN > 0:
				skipN -= 1
				continue

			p, n = checkToken(tks, i, token)
			if n < 0:
				n = 0
			skipN += n
			checkPassed &= p

	return (tks, checkPassed)


def checkToken(tokens: Sequence[Token], idx: int, token: Token) -> tuple[bool, int]:
	"""
		:return: check passed, how many to skip
	"""
	i = idx
	success = True
	if token.kind == TokenKind.LPAREN:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.RPAREN:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.LBRACE:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.RBRACE:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.LBRACKET:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.RBRACKET:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.DOT:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.COLON:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.COMMA:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.SEMICOLON:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.PLUS:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.PLUS_PLUS:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.PLUS_EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.MINUS:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.MINUS_MINUS:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.MINUS_EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.ASTERISK:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.ASTERISK_EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.SLASH:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.SLASH_EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.AMPERSAND:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.AMPERSAND_AMPERSAND:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.PIPE:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.PIPE_PIPE:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.BANG:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.BANG_EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.EQUAL_EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.GREATER:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.GREATER_EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.LESSER:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.LESSER_EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.CARET:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.CARET_EQUAL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.IDENTIFIER:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.STRING:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.INTEGER:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.FLOAT:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.LET:
		while tokens[i] != TokenKind.SEMICOLON and i < len(tokens):
			i += 1
			# Check variable name is identifier
			varName = tokens[i]
			sccss = True
			if varName.kind != TokenKind.IDENTIFIER:
				print(Failure((f"Expected variable name, got {varName.kind}", varName)))
				success &= False
				i += 1
				if tokens[i].kind == TokenKind.SEMICOLON:
					i += 1
					break
				elif tokens[i].kind == TokenKind.EQUAL:
					i += 1
					if tokens[i].kind not in (TokenKind.NULL, TokenKind.TRUE, TokenKind.FALSE, TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.STRING):
						print(Failure((
							f"Expected one of: "
							f"{', '.join(str(k) for k in (TokenKind.NULL, TokenKind.TRUE, TokenKind.FALSE, TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.STRING))}; "
							f"got {tokens[i].kind}",
							tokens[i],
						)))
						sccss &= False
					else:
						i += 1
						continue
				elif tokens[i].kind == TokenKind.COMMA:
					i += 1
					continue
				else:
					print(Failure((
						f"Expected one of: {TokenKind.SEMICOLON}, {TokenKind.EQUAL}, {TokenKind.COMMA}; got {tokens[i + 1].kind}",
						tokens[i + 1],
					)))
					i += 1
					continue

			if sccss is False or success is False:
				return (False, i - idx)

			i += 1
			# Check variable value (if it exists)
			if tokens[i].kind == TokenKind.SEMICOLON:
				# no value and end of declarations
				continue
			elif tokens[i].kind == TokenKind.COMMA:
				# no value but more declarations
				i += 1
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
					print(Failure((
						f"Expected one of: "
						f"{', '.join(str(k) for k in (TokenKind.NULL, TokenKind.TRUE, TokenKind.FALSE, TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.STRING, TokenKind.IDENTIFIER))}; "
						f"got {tokens[i].kind}",
						tokens[i],
					)))
					success &= False
				else:
					i += 1
					continue
			else:
				print(Failure((
					f"Expected one of {', '.join(str(k) for k in (TokenKind.SEMICOLON, TokenKind.COMMA, TokenKind.EQUAL))}",
					tokens[i]
				)))
				success &= False

		if i == len(tokens):
			print(Failure(("Expected semicolon after variable declaration(s)", tokens[idx])))
			success &= False

	elif token.kind == TokenKind.IF:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.ELSE:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.TRUE:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.FALSE:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.NULL:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.WHILE:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.DO:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.FOR:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.DEF:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.RETURN:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.CLASS:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.THIS:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.SUPER:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.PRINT:
		print(Failure((f"checking {token.kind} is not yet implemented", token)))
		return (False, 1)
	elif token.kind == TokenKind.EOF:
		if idx + 1 != len(tokens):
			print(Failure(("Found more tokens after EOF", tokens[idx + 1])))
			success &= False
	else:
		print(Failure(("Unexpected token", token)))
		return (False, 1)

	return (success, i - idx)
