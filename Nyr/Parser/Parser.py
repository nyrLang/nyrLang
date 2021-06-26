from typing import Any

import Nyr.Parser.Node as Node
from Nyr.Parser.Tokenizer import Tokenizer


class Parser:
	string: str
	tokenizer: Tokenizer
	lookahead: Node

	def __init__(self):
		self.tokenizer = Tokenizer()

	@staticmethod
	def _isLiteral(tokenType) -> bool:
		return tokenType in ["INTEGER", "FLOAT", "STRING", "true", "false", "null"]

	@staticmethod
	def _isAssignmentOperator(tokenType):
		return tokenType in ["SIMPLE_ASSIGN", "COMPLEX_ASSIGN"]

	@staticmethod
	def _checkValidAssignmentTarget(node: Node.Node) -> Node.Node:
		if node.type in ["Identifier", "MemberExpression"]:
			return node
		else:
			raise SyntaxError("Invalid left-hand side in assignment expression")

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
		statementList: list[Node.Node] = [self.Statement()]

		while self.lookahead and self.lookahead.type != stopLookahead:
			statementList.append(self.Statement())

		return statementList

	def Statement(self) -> Node.Node:
		if self.lookahead is not None:
			if self.lookahead.type == ";": return self.EmptyStatement()
			elif self.lookahead.type == "{": return self.BlockStatement()
			elif self.lookahead.type == "let": return self.VariableStatement()
			elif self.lookahead.type == "if": return self.IfStatement()
			elif self.lookahead.type == "while": return self.IterationStatement()
			elif self.lookahead.type == "do": return self.IterationStatement()
			elif self.lookahead.type == "for": return self.IterationStatement()
			elif self.lookahead.type == "def": return self.FunctionDeclaration()
			elif self.lookahead.type == "return": return self.ReturnStatement()
			else: return self.ExpressionStatement()

	def FunctionDeclaration(self) -> Node.FunctionDeclaration:
		""" FunctionDeclaration
			: 'def' Identifier '(' OptFormalParameterList ')' BlockStatement
			;
		"""
		self._eat("def")
		name = self.Identifier()

		self._eat("(")
		params: list[Node.Node] = self.FormalParameterList() if self.lookahead.type != ")" else []
		self._eat(")")

		body = self.BlockStatement()

		return Node.FunctionDeclaration(name, params, body)

	def FormalParameterList(self) -> list[Node.Node]:
		""" FormalParameterList
			: Identifier
			| FormalParameterList ',' Identifier
			;
		"""
		params: list[Node.Node] = []

		while True:
			params.append(self.Identifier())

			if self.lookahead.type == ",":
				self._eat(",")
				continue
			else:
				break

		return params

	def ReturnStatement(self) -> Node.ReturnStatement:
		""" ReturnStatement
			: 'return' OptExpression ';'
			;
		"""
		self._eat("return")

		argument = self.Expression() if self.lookahead.type != ";" else None

		self._eat(";")

		return Node.ReturnStatement(argument)

	def IterationStatement(self) -> Node.Node:
		if self.lookahead.type == "while":
			return self.WhileStatement()
		elif self.lookahead.type == "do":
			return self.DoWhileStatement()
		elif self.lookahead.type == "for":
			return self.ForStatement()

	def WhileStatement(self) -> Node.WhileStatement:
		self._eat("while")

		self._eat("(")
		test = self.Expression()
		self._eat(")")

		body = self.Statement()

		return Node.WhileStatement("WhileStatement", test=test, body=body)

	def DoWhileStatement(self) -> Node.WhileStatement:
		self._eat("do")

		body = self.Statement()

		self._eat("while")
		self._eat("(")
		test = self.Expression()
		self._eat(")")
		self._eat(";")

		return Node.WhileStatement("DoWhileStatement", body=body, test=test)

	def ForStatement(self) -> Node.ForStatement:
		self._eat("for")
		self._eat("(")

		init = self.ForStatementInit() if self.lookahead.type != ";" else None
		self._eat(";")

		test = self.Expression() if self.lookahead.type != ";" else None
		self._eat(";")

		update = self.Expression() if self.lookahead.type != ")" else None
		self._eat(")")

		body = self.Statement()

		return Node.ForStatement(init, test, update, body)

	def ForStatementInit(self) -> Node.Node:
		if self.lookahead.type == "let":
			return self.VariableStatementInit()
		return self.Expression()

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

	def VariableStatementInit(self) -> Node.VariableStatement:
		self._eat("let")
		declarations = self.VariableDeclarationList()

		return Node.VariableStatement(declarations)

	def VariableStatement(self) -> Node.VariableStatement:
		variableStatement = self.VariableStatementInit()
		self._eat(";")
		return variableStatement

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

	def AssignmentExpression(self) -> Node.Node:
		left = self.LogicalORExpression()

		if not self._isAssignmentOperator(self.lookahead.type):
			return left

		return Node.ComplexExpression(
			"AssignmentExpression",
			self.AssignmentOperator().value,
			self._checkValidAssignmentTarget(left),
			self.AssignmentExpression(),
		)

	def AssignmentOperator(self) -> Node.Node:
		""" AssignmentOperator
			: SIMPLE_ASSIGN
			| COMPLEX_ASSIGN
			;
		"""
		if self.lookahead.type == "SIMPLE_ASSIGN":
			return self._eat("SIMPLE_ASSIGN")
		return self._eat("COMPLEX_ASSIGN")

	def LogicalExpression(self, builderName, operatorToken) -> Node.Node:
		builder = getattr(self, builderName)

		left = builder()

		while self.lookahead.type == operatorToken:
			operator = self._eat(operatorToken).value

			right = builder()

			left = Node.ComplexExpression(
				"LogicalExpression",
				operator,
				left,
				right,
			)

		return left

	def LogicalORExpression(self) -> Node.Node:
		return self.LogicalExpression("LogicalANDExpression", "LOGICAL_OR")

	def LogicalANDExpression(self) -> Node.Node:
		return self.LogicalExpression("EqualityExpression", "LOGICAL_AND")

	def LeftHandSideExpression(self) -> Node.Node:
		""" LeftHandSideExpression
			: CallMemberExpression
			;
		"""
		return self.CallMemberExpression()

	def CallMemberExpression(self) -> Node.Node:
		""" CallMemberExpression
			: MemberExpression
			| CallExpression
			;
		"""

		member = self.MemberExpression()

		if self.lookahead.type == "(":
			return self.CallExpression(member)

		return member

	def CallExpression(self, callee: Node.Node) -> Node.Node:
		""" CallExpression
			: Callee Arguments
			;

			:argument callee
			: MemberExpression
			| CallExpresion
			;
		"""

		callExpression = Node.CallExpression(callee, self.Arguments())

		if self.lookahead.type == "(":
			callExpression = self.CallExpression(callExpression)

		return callExpression

	def Arguments(self) -> list[Node.Node]:
		""" Arguments
			: '(' OptArgumentList ')'
			;
		"""

		self._eat("(")
		argumentList: list[Node.Node] = self.ArgumentList() if self.lookahead.type != ")" else []
		self._eat(")")

		return argumentList

	def ArgumentList(self) -> list[Node.Node]:
		""" ArgumentList
			: AssignmentExpression
			| ArgumentList ',' AssignmentExpression
			;
		"""

		argumentList: list[Node.Node] = []

		while True:
			argumentList.append(self.AssignmentExpression())
			if self.lookahead.type == ",":
				self._eat(",")
			else:
				break

		return argumentList

	def MemberExpression(self) -> Node.Node:
		""" MemberExpression
			: PrimaryExpression
			| MemberExpresssion '.' Identifier
			| MemberExpression '[' Expression ']'
			;
		"""
		object_ = self.PrimaryExpression()

		while self.lookahead.type in [".", "["]:
			# MemberExpression '.' Identifier
			if self.lookahead.type == ".":
				self._eat(".")
				property_ = self.Identifier()

				object_ = Node.MemberExpression(False, object_, property_)

			# MemberExpression '[' Expression ']'
			if self.lookahead.type == "[":
				self._eat("[")
				property_ = self.Expression()
				self._eat("]")

				object_ = Node.MemberExpression(True, object_, property_)

		return object_

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
		builder = getattr(self, builderName)

		left = builder()

		while self.lookahead.type == operatorToken:
			operator = self._eat(operatorToken).value

			right = builder()

			left = Node.ComplexExpression(
				"BinaryExpression",
				operator,
				left,
				right,
			)

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
		""" PromaryExpression
			: Literal
			| ParenthesizedExpression
			| Identifier
			;
		"""
		if self._isLiteral(self.lookahead.type):
			return self.Literal()

		if self.lookahead.type == "(":
			return self.ParenthesizedExpression()
		elif self.lookahead.type == "IDENTIFIER":
			return self.Identifier()
		else:
			return self.LeftHandSideExpression()

	def ParenthesizedExpression(self) -> Node.Node:
		self._eat("(")
		expression = self.Expression()
		self._eat(")")

		return expression

	def Literal(self) -> Node.Literal:
		if self.lookahead.type == "INTEGER":
			token = self._eat("INTEGER")
			return Node.Literal("IntegerLiteral", int(token.value))
		elif self.lookahead.type == "FLOAT":
			token = self._eat("FLOAT")
			return Node.Literal("FloatLiteral", float(token.value))
		elif self.lookahead.type == "STRING":
			token = self._eat("STRING")
			return Node.Literal("StringLiteral", str(token.value)[1: -1])
		elif self.lookahead.type == "true":
			self._eat("true")
			return Node.Literal("BooleanLiteral", True)
		elif self.lookahead.type == "false":
			self._eat("false")
			return Node.Literal("BooleanLiteral", False)
		elif self.lookahead.type == "null":
			self._eat("null")
			return Node.Literal("NullLiteral", None)
		else:
			raise SyntaxError("Literal: unexpected literal production")
