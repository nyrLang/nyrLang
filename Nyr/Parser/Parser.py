from typing import Any

import Nyr.Parser.Node as Node
from Nyr.Parser.Tokenizer import Tokenizer


class Parser:
	string: str
	tokenizer: Tokenizer
	lookahead: Node

	def __init__(self):
		self.tokenizer = Tokenizer()

	def parse(self, string: str) -> Node.Program:
		self.string = string
		self.tokenizer.init(string)

		self.lookahead = self.tokenizer.getNextToken()

		return self.Program()

	def Program(self) -> Node.Program:
		return Node.Program(self.StatementList())

	def _eat(self, tokenType: str) -> Node.Node:
		token = self.lookahead

		if not token:
			raise SyntaxError(f"Unexpected end of input, exprected {tokenType}")

		if token.type != tokenType:
			raise SyntaxError(f'Unexpected token: "{token.value}", expected: "{tokenType}"')

		self.lookahead = self.tokenizer.getNextToken()

		return token

	def StatementList(self, stopLookahead: Any = None) -> list[Node.Node]:
		if not self.lookahead: return []
		statementList: list[Node] = [self.Statement()]

		while self.lookahead and self.lookahead.type != stopLookahead:
			statementList.append(self.Statement())

		return statementList

	def Statement(self) -> Node.Node:
		if self.lookahead is not None:
			if self.lookahead.type == ";": return self.EmptyStatement()
			elif self.lookahead.type == "{": return self.BlockStatement()
			elif self.lookahead.type == "let": return self.VariableStatement()
			elif self.lookahead.type == "if": return self.IfStatement()
			else: return self.ExpressionStatement()

	def IfStatement(self) -> Node.IfStatement:
		self._eat("if")
		self._eat("(")

		test = self.Expression()

		self._eat(")")

		consequent = self.Statement()

		if self.lookahead and self.lookahead.type == "else":
			self._eat("else")
			alternative = self.Statement()
		else:
			alternative = None

		return Node.IfStatement(test, consequent, alternative)

	def VariableStatement(self) -> Node.VariableStatement:
		self._eat("let")
		declarations = self.VariableDeclarationList()
		self._eat(";")
		return Node.VariableStatement(declarations)

	def VariableDeclarationList(self) -> list[Node.Node]:
		declarations: list[Node.Node] = []

		while True:
			declarations.append(self.VariableDeclaration())
			if self.lookahead.type == ",":
				self._eat(",")
			else:
				break

		return declarations

	def VariableDeclaration(self) -> Node.VariableDeclaration:
		id_ = self.Identifier()

		if self.lookahead.type != ";" and self.lookahead.type != ",":
			init = self.VariableInitializer()
		else:
			init = None

		return Node.VariableDeclaration(id_, init)

	def VariableInitializer(self) -> Node.Node:
		self._eat("SIMPLE_ASSIGN")
		return self.AssignmentExpression()

	def EmptyStatement(self) -> Node.EmptyStatement:
		self._eat(";")
		return Node.EmptyStatement()

	def BlockStatement(self) -> Node.BlockStatement:
		self._eat("{")

		body: list[Node.Node] = self.StatementList("}") if self.lookahead.type != "}" else []

		self._eat("}")

		return Node.BlockStatement(body)

	def ExpressionStatement(self) -> Node.ExpressionStatement:
		expression = self.Expression()
		self._eat(";")

		return Node.ExpressionStatement(expression)

	def Expression(self) -> Node.Node:
		return self.AssignmentExpression()

	@staticmethod
	def _isAssignmentOperator(tokenType):
		return tokenType in ["SIMPLE_ASSIGN", "COMPLEX_ASSIGN"]

	@staticmethod
	def _checkValidAssignmentTarget(node: Node.Node) -> Node.Node:
		if node.type == "Identifier":
			return node
		else:
			raise SyntaxError("Invalid left-hand side in assignment expression")

	def AssignmentExpression(self) -> Node.Node:
		left = self.LogicalORExpression()

		if not self._isAssignmentOperator(self.lookahead.type):
			return left

		return Node.AssignmentExpression(
			self.AssignmentOperator().value,
			self._checkValidAssignmentTarget(left),
			self.AssignmentExpression(),
		)

	def AssignmentOperator(self) -> Node.Node:
		if self.lookahead.type == "SIMPLE_ASSIGN":
			return self._eat("SIMPLE_ASSIGN")
		return self._eat("COMPLEX_ASSIGN")

	def _LogicalExpression(self, builderName, operatorToken) -> Node.Node:
		if builderName == "LogicalANDExpression":
			builder = self.LogicalANDExpression
		elif builderName == "EqualityExpression":
			builder = self.EqualityExpression
		else: raise Exception(f"Unknown builderName: {builderName}")

		left = builder()

		while self.lookahead.type == operatorToken:
			operator = self._eat(operatorToken).value

			right = builder()

			left = Node.LogicalExpression(operator, left, right)

		return left

	def LogicalORExpression(self) -> Node.Node:
		return self._LogicalExpression("LogicalANDExpression", "LOGICAL_OR")

	def LogicalANDExpression(self) -> Node.Node:
		return self._LogicalExpression("EqualityExpression", "LOGICAL_AND")

	def LeftHandSideExpression(self) -> Node.Node:
		return self.PrimaryExpression()

	def Identifier(self) -> Node.Identifier:
		name = self._eat("IDENTIFIER").value

		return Node.Identifier(name)

	def EqualityExpression(self) -> Node.Node:
		return self.BinaryExpression("RelationalExpression", "EQUALITY_OPERATOR")

	def RelationalExpression(self) -> Node.Node:
		return self.BinaryExpression("AdditiveExpression", "RELATIONAL_OPERATOR")

	def AdditiveExpression(self) -> Node.Node:
		return self.BinaryExpression("MultiplicativeExpression", "ADDITIVE_OPERATOR")

	def MultiplicativeExpression(self) -> Node.Node:
		return self.BinaryExpression("UnaryExpression", "MULTIPLICATIVE_OPERATOR")

	def BinaryExpression(self, builderName, operatorToken) -> Node.Node:
		if builderName == "RelationalExpression":
			builder = self.RelationalExpression
		elif builderName == "AdditiveExpression":
			builder = self.AdditiveExpression
		elif builderName == "MultiplicativeExpression":
			builder = self.MultiplicativeExpression
		elif builderName == "PrimaryExpression":
			builder = self.PrimaryExpression
		elif builderName == "UnaryExpression":
			builder = self.UnaryExpression
		else: raise Exception(f"Unknown builderName: {builderName}")

		left = builder()

		while self.lookahead.type == operatorToken:
			operator = self._eat(operatorToken).value

			right = builder()

			left = Node.BinaryExpression(operator, left, right)

		return left

	def UnaryExpression(self) -> Node.Node:
		operator = None

		if self.lookahead.type == "ADDITIVE_OPERATOR":
			operator = self._eat("ADDITIVE_OPERATOR").value
		elif self.lookahead.type == "LOGICAL_NOT":
			operator = self._eat("LOGICAL_NOT").value

		if operator is not None:
			return Node.UnaryExpression(operator, self.UnaryExpression())

		return self.LeftHandSideExpression()

	def PrimaryExpression(self) -> Node.Node:
		if self._isLiteral(self.lookahead.type):
			return self.Literal()

		if self.lookahead.type == "(":
			return self.ParenthesizedExpression()
		elif self.lookahead.type == "IDENTIFIER":
			return self.Identifier()
		else:
			return self.LeftHandSideExpression()

	def _isLiteral(self, tokenType) -> bool:
		return tokenType in ["INTEGER", "FLOAT", "STRING", "true", "false", "null"]

	def ParenthesizedExpression(self) -> Node.Node:
		self._eat("(")
		expression = self.Expression()
		self._eat(")")

		return expression

	def Literal(self) -> Node.Node:
		if self.lookahead.type == "INTEGER":
			return self.IntegerLiteral()
		elif self.lookahead.type == "FLOAT":
			return self.FloatLiteral()
		elif self.lookahead.type == "STRING":
			return self.StringLiteral()
		elif self.lookahead.type == "true":
			return self.BooleanLiteral(True)
		elif self.lookahead.type == "false":
			return self.BooleanLiteral(False)
		elif self.lookahead.type == "null":
			return self.NullLiteral()
		else:
			raise SyntaxError("Literal: unexpected literal production")

	def NullLiteral(self) -> Node.NullLiteral:
		self._eat("null")

		return Node.NullLiteral()

	def BooleanLiteral(self, value: bool) -> Node.BooleanLiteral:
		self._eat("true" if value else "false")

		return Node.BooleanLiteral(value)

	def IntegerLiteral(self) -> Node.IntegerLiteral:
		token = self._eat("INTEGER")

		return Node.IntegerLiteral(int(token.value))

	def FloatLiteral(self) -> Node.FloatLiteral:
		token = self._eat("FLOAT")

		return Node.FloatLiteral(float(token.value))

	def StringLiteral(self) -> Node.StringLiteral:
		token = self._eat("STRING")

		return Node.StringLiteral(str(token.value)[1: -1])
