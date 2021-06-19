from Nyr.Node import Node
from Nyr.Tokenizer import Token
from Nyr.Tokenizer import Tokenizer


class Parser:
	string: str
	lookahead = None
	tokenizer: Tokenizer

	def __init__(self):
		self.string = ""
		self.tokenizer = Tokenizer()

	def parse(self, string: str):
		self.string: str = string
		self.tokenizer.init(string)

		self.lookahead = self.tokenizer.getNextToken()

		return self.Program()

	def _eat(self, tokenType: Token):
		token = self.lookahead

		if not token:
			raise SyntaxError(f'Unexpected end of input, expected: "{tokenType}"')
		elif token.get("type") != tokenType:
			raise SyntaxError(f'Unexpected token: "{token.get("value")}", expected: "{tokenType}"')

		self.lookahead = self.tokenizer.getNextToken()

		return token

	def Program(self):
		""" Program
			: StatementList
			;
		"""
		return {
			"type": Node.Program,
			"body": self.StatementList(),
		}

	def StatementList(self):
		""" StatementList
			: Statement
			| StatementList Statement
			;
		"""
		statementList: list = [self.Statement()]

		while self.lookahead:
			statementList.append(self.Statement())

		return statementList

	def Statement(self):
		""" Statement
			: ExpressionStatement
			;
		"""
		return self.ExpressionStatement()

	def ExpressionStatement(self):
		""" ExpressionStatement
			: Expression ';'
			;
		"""
		expression = self.Expression()

		self._eat(Token.Semicolon)

		return {
			"type": Node.ExpressionStatement,
			"expression": expression,
		}

	def Expression(self):
		""" Expression
			: Literal
			;
		"""
		return self.Literal()

	def Literal(self):
		""" Literal
			: NumericLiteral
			| StringLiteral
			;
		"""

		if not self.lookahead:
			return None
		elif self.lookahead.get("type") == Token.NoneToken:
			return None
		elif self.lookahead.get("type") == Token.Number:
			return self.NumericLiteral()
		elif self.lookahead.get("type") == Token.String:
			return self.StringLiteral()
		else:
			raise SyntaxError("Literal: unexpected literal production")

	def StringLiteral(self):
		""" StringLiteral
			: STRING
			;
		"""
		token = self._eat(Token.String)
		return {
			"type": Node.StringLiteral,
			"value": token.get("value")[1: -1],
		}

	def NumericLiteral(self):
		""" NumericLiteral
			: NUMBER
			;
		"""
		token = self._eat(Token.Number)
		return {
			"type": Node.NumericLiteral,
			"value": token.get("value"),
		}
