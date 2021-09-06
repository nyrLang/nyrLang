from typing import Any

from nyr.parser import node
from nyr.parser.tokenizer import Token
from nyr.parser.tokenizer import Tokenizer


class Parser:
	string: str
	tokenizer: Tokenizer
	lookahead: Token
	tokens: tuple[Token]
	tkIndex: int = 0
	fns: dict[str, dict[str, Any]] = dict()

	def __init__(self):
		self.tokenizer = Tokenizer()

	def _reset(self):
		self.string = ""
		self.lookahead = None
		self.tokens = tuple()
		self.tkIndex = 0
		self.fns = {}

	@staticmethod
	def _isLiteral(tokenType) -> bool:
		return tokenType in ("INTEGER", "FLOAT", "STRING", "true", "false", "null")

	@staticmethod
	def _isAssignmentOperator(tokenType):
		return tokenType in ("SIMPLE_ASSIGN", "COMPLEX_ASSIGN")

	@staticmethod
	def _checkValidAssignmentTarget(node: node.Node) -> node.Node:
		if node.type in ("Identifier", "MemberExpression"):
			return node
		else:
			raise SyntaxError(f"Invalid left-hand side in assignment expression: {node}; expected: Identifier, MemberExpression")

	def getNextToken(self) -> Token:
		tk = self.tokens[self.tkIndex]
		self.tkIndex += 1
		return tk

	def hasMoreTokens(self) -> bool:
		return self.tkIndex == len(self.tokens) and self.tokens[self.tkIndex - 1].type == "EOF"

	def parse(self, string: str) -> node.Program:
		self._reset()
		self.string = string.strip()
		self.tokenizer.init(self.string)

		self.tokens = self.tokenizer.getTokens()
		self.lookahead = self.getNextToken()

		if self.lookahead.type == "EOF":
			return node.Program([])

		return self.Program()

	def Program(self) -> node.Program:
		return node.Program(self.StatementList())

	def _eat(self, tokenType: str) -> Token:
		token = self.lookahead

		if token.type == tokenType:
			self.lookahead = self.getNextToken()
			return token

		if not self.hasMoreTokens() is True or token.type == "EOF":
			raise SyntaxError(f'Unexpected end of input, expected "{tokenType}"')

		raise SyntaxError(f'Unexpected token: "{token}", expected: "{tokenType}"')  # pragma: no cover

	def StatementList(self, stopLookahead: Any = None) -> list[node.Node]:
		statementList: list[node.Node] = [self.Statement()]

		while self.lookahead.type not in [stopLookahead, "EOF"]:
			statementList.append(self.Statement())

		return statementList

	def Statement(self) -> node.Node:
		""" Statement
			: ExpressionStatement
			| BlockStatement
			| EmptyStatement
			| VariableStatement
			| IfStatement
			| IterationStatement
			| FunctionDeclaration
			| ReturnStatement
			| ClassDeclaration
			;
		"""
		assert self.lookahead is not None

		if self.lookahead.type == ";":
			return self.EmptyStatement()
		elif self.lookahead.type == "{":
			return self.BlockStatement()
		elif self.lookahead.type == "let":
			return self.VariableStatement()
		elif self.lookahead.type == "if":
			return self.IfStatement()
		elif self.lookahead.type in ("while", "do", "for"):
			return self.IterationStatement()
		elif self.lookahead.type == "def":
			return self.FunctionDeclaration()
		elif self.lookahead.type == "return":
			return self.ReturnStatement()
		elif self.lookahead.type == "class":
			return self.ClassDeclaration()
		else:
			return self.ExpressionStatement()

	def SuperExpression(self) -> node.SuperExpression:
		""" Super
			: 'super'
			;
		"""

		self._eat("super")

		return node.SuperExpression()

	def ThisExpression(self) -> node.ThisExpression:
		""" ThisExpression
			: 'this'
			;
		"""

		self._eat("this")

		return node.ThisExpression()

	def ClassDeclaration(self) -> node.ClassDeclaration:
		""" ClassDeclaration
			: 'class' Identifier OptClassExtends BlockStatement
		"""

		self._eat("class")
		id_ = self.Identifier()

		superClass = self.ClassExtends() if self.lookahead.type == ":" else None

		body = self.BlockStatement()

		return node.ClassDeclaration(id_, superClass, body)

	def ClassExtends(self) -> node.Identifier:
		""" ClassExtends
			: ':' Identifier
			;
		"""

		self._eat(":")

		name = self.Identifier()

		return name

	def FunctionDeclaration(self) -> node.FunctionDeclaration:
		""" FunctionDeclaration
			: 'def' Identifier '(' OptFormalParameterList ')' BlockStatement
			;
		"""

		self._eat("def")
		name = self.Identifier()
		self.fns.update({name.name: {}})

		self._eat("(")
		params: list[node.Node] = self.FormalParameterList() if self.lookahead.type != ")" else []
		self._eat(")")
		self.fns[name.name].update({"args": params})

		body = self.BlockStatement()
		self.fns[name.name].update({"body": body})

		return node.FunctionDeclaration(name, params, body)

	def FormalParameterList(self) -> list[node.Node]:
		""" FormalParameterList
			: Identifier
			| FormalParameterList ',' Identifier
			;
		"""

		params: list[node.Node] = [
			self.Identifier(),
		]

		while self.lookahead.type == ",":
			self._eat(",")
			params.append(self.Identifier())

		return params

	def ReturnStatement(self) -> node.ReturnStatement:
		""" ReturnStatement
			: 'return' OptExpression ';'
			;
		"""

		self._eat("return")

		argument = self.Expression() if self.lookahead.type != ";" else None

		self._eat(";")

		return node.ReturnStatement(argument)

	def IterationStatement(self) -> node.Node:
		if self.lookahead.type == "while": return self.WhileStatement()
		elif self.lookahead.type == "do": return self.DoWhileStatement()
		elif self.lookahead.type == "for": return self.ForStatement()
		else:  # pragma: no cover
			raise Exception(f"Unknown IterationStatement {self.lookahead.type}")

	def WhileStatement(self) -> node.WhileStatement:
		self._eat("while")

		self._eat("(")
		test = self.Expression()
		self._eat(")")

		body = self.Statement()

		return node.WhileStatement(test=test, body=body)

	def DoWhileStatement(self) -> node.DoWhileStatement:
		self._eat("do")

		body = self.Statement()

		self._eat("while")
		self._eat("(")
		test = self.Expression()
		self._eat(")")
		self._eat(";")

		return node.DoWhileStatement(body=body, test=test)

	def ForStatement(self) -> node.ForStatement:
		self._eat("for")
		self._eat("(")

		init = self.ForStatementInit() if self.lookahead.type != ";" else None
		self._eat(";")

		test = self.Expression() if self.lookahead.type != ";" else None
		self._eat(";")

		update = self.Expression() if self.lookahead.type != ")" else None
		self._eat(")")

		body = self.Statement()

		return node.ForStatement(init, test, update, body)

	def ForStatementInit(self) -> node.Node:
		if self.lookahead.type == "let":
			return self.VariableStatementInit()
		return self.Expression()

	def IfStatement(self) -> node.IfStatement:
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

		return node.IfStatement(test, consequent, alternative)

	def VariableStatementInit(self) -> node.VariableStatement:
		self._eat("let")
		declarations = self.VariableDeclarationList()

		return node.VariableStatement(declarations)

	def VariableStatement(self) -> node.VariableStatement:
		variableStatement = self.VariableStatementInit()
		self._eat(";")
		return variableStatement

	def VariableDeclarationList(self) -> list[node.Node]:
		declarations: list[node.Node] = [
			self.VariableDeclaration(),
		]

		while self.lookahead.type == ",":
			self._eat(",")
			declarations.append(self.VariableDeclaration())

		return declarations

	def VariableDeclaration(self) -> node.VariableDeclaration:
		id_ = self.Identifier()

		if self.lookahead.type != ";" and self.lookahead.type != ",":
			init = self.VariableInitializer()
		else:
			init = None

		return node.VariableDeclaration(id_, init)

	def VariableInitializer(self) -> node.Node:
		self._eat("SIMPLE_ASSIGN")
		return self.AssignmentExpression()

	def EmptyStatement(self) -> node.EmptyStatement:
		self._eat(";")
		return node.EmptyStatement()

	def BlockStatement(self) -> node.BlockStatement:
		self._eat("{")

		body: list[node.Node] = self.StatementList("}") if self.lookahead.type != "}" else []

		self._eat("}")

		return node.BlockStatement(body)

	def ExpressionStatement(self) -> node.ExpressionStatement:
		expression = self.Expression()
		self._eat(";")

		return node.ExpressionStatement(expression)

	def Expression(self) -> node.Node:
		return self.AssignmentExpression()

	def AssignmentExpression(self) -> node.Node:
		left = self.LogicalORExpression()

		if not self._isAssignmentOperator(self.lookahead.type):
			return left

		return node.ComplexExpression(
			"AssignmentExpression",
			self.AssignmentOperator().value,
			self._checkValidAssignmentTarget(left),
			self.AssignmentExpression(),
		)

	def AssignmentOperator(self) -> Token:
		""" AssignmentOperator
			: SIMPLE_ASSIGN
			| COMPLEX_ASSIGN
			;
		"""
		if self.lookahead.type == "SIMPLE_ASSIGN":
			return self._eat("SIMPLE_ASSIGN")
		return self._eat("COMPLEX_ASSIGN")

	def LogicalExpression(self, builderName, operatorToken) -> node.Node:
		builder = getattr(self, builderName)

		left = builder()

		while self.lookahead.type == operatorToken:
			operator = self._eat(operatorToken).value

			right = builder()

			left = node.ComplexExpression(
				"LogicalExpression",
				operator,
				left,
				right,
			)

		return left

	def LogicalORExpression(self) -> node.Node:
		return self.LogicalExpression("LogicalANDExpression", "LOGICAL_OR")

	def LogicalANDExpression(self) -> node.Node:
		return self.LogicalExpression("BitwiseORExpression", "LOGICAL_AND")

	def BitwiseExpression(self, builderName, operatorToken) -> node.Node:
		builder = getattr(self, builderName)

		left = builder()

		while self.lookahead.type == operatorToken:
			operator = self._eat(operatorToken).value

			right = builder()

			left = node.ComplexExpression(
				"BitwiseExpression",
				operator,
				left,
				right,
			)

		return left

	def BitwiseORExpression(self) -> node.Node:
		return self.BitwiseExpression("BitwiseXORExpression", "BITWISE_OR")

	def BitwiseXORExpression(self) -> node.Node:
		return self.BitwiseExpression("BitwiseANDExpression", "BITWISE_XOR")

	def BitwiseANDExpression(self) -> node.Node:
		return self.BitwiseExpression("EqualityExpression", "BITWISE_AND")

	def LeftHandSideExpression(self) -> node.Node:
		""" LeftHandSideExpression
			: CallMemberExpression
			;
		"""
		return self.CallMemberExpression()

	def CallMemberExpression(self) -> node.Node:
		""" CallMemberExpression
			: MemberExpression
			| CallExpression
			;
		"""

		if self.lookahead.type == "super":
			return self.CallExpression(self.SuperExpression())

		member = self.MemberExpression()

		if self.lookahead.type == "(":
			return self.CallExpression(member)

		return member

	def CallExpression(self, callee: node.Node) -> node.Node:
		""" CallExpression
			: Callee Arguments
			;

			:argument callee
			: MemberExpression
			| CallExpresion
			;
		"""

		fn = None
		if isinstance(callee, node.Identifier):
			fn = self.fns.get(callee.name, None)
		callExpression = node.CallExpression(callee, self.Arguments(), fn)

		if self.lookahead.type == "(":
			callExpression = self.CallExpression(callExpression)

		return callExpression

	def Arguments(self) -> list[node.Node]:
		""" Arguments
			: '(' OptArgumentList ')'
			;
		"""

		self._eat("(")
		argumentList: list[node.Node] = self.ArgumentList() if self.lookahead.type != ")" else []
		self._eat(")")

		return argumentList

	def ArgumentList(self) -> list[node.Node]:
		""" ArgumentList
			: AssignmentExpression
			| ArgumentList ',' AssignmentExpression
			;
		"""
		argumentList: list[node.Node] = [
			self.AssignmentExpression(),
		]

		while self.lookahead.type == ",":
			self._eat(",")
			argumentList.append(self.AssignmentExpression())

		return argumentList

	def MemberExpression(self) -> node.Node:
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

				object_ = node.MemberExpression(False, object_, property_)

			# MemberExpression '[' Expression ']'
			if self.lookahead.type == "[":
				self._eat("[")
				property_ = self.Expression()
				self._eat("]")

				object_ = node.MemberExpression(True, object_, property_)

		return object_

	def Identifier(self) -> node.Identifier:
		name = self._eat("IDENTIFIER").value

		return node.Identifier(name)

	def EqualityExpression(self) -> node.Node:
		return self.BinaryExpression("RelationalExpression", "EQUALITY_OPERATOR")

	def RelationalExpression(self) -> node.Node:
		return self.BinaryExpression("AdditiveExpression", "RELATIONAL_OPERATOR")

	def AdditiveExpression(self) -> node.Node:
		return self.BinaryExpression("MultiplicativeExpression", "ADDITIVE_OPERATOR")

	def MultiplicativeExpression(self) -> node.Node:
		return self.BinaryExpression("UnaryExpression", "MULTIPLICATIVE_OPERATOR")

	def BinaryExpression(self, builderName, operatorToken) -> node.Node:
		builder = getattr(self, builderName)

		left = builder()

		while self.lookahead.type == operatorToken:
			operator = self._eat(operatorToken).value

			right = builder()

			left = node.ComplexExpression(
				"BinaryExpression",
				operator,
				left,
				right,
			)

		return left

	def UnaryExpression(self) -> node.Node:
		if self.lookahead.type == "ADDITIVE_OPERATOR":
			operator = self._eat("ADDITIVE_OPERATOR").value
		elif self.lookahead.type == "LOGICAL_NOT":
			operator = self._eat("LOGICAL_NOT").value
		else:
			operator = None

		if operator is not None:
			return node.UnaryExpression(operator, self.UnaryExpression())

		return self.LeftHandSideExpression()

	def PrimaryExpression(self) -> node.Node:
		""" PromaryExpression
			: Literal
			| ParenthesizedExpression
			| Identifier
			| ThisExpression
			;
		"""
		if self._isLiteral(self.lookahead.type):
			return self.Literal()

		if self.lookahead.type == "(":
			return self.ParenthesizedExpression()
		elif self.lookahead.type == "IDENTIFIER":
			return self.Identifier()
		elif self.lookahead.type == "this":
			return self.ThisExpression()
		else:
			return self.LeftHandSideExpression()

	def ParenthesizedExpression(self) -> node.Node:
		self._eat("(")
		expression = self.Expression()
		self._eat(")")

		return expression

	def Literal(self) -> node.Literal:
		if self.lookahead.type == "INTEGER":
			token = self._eat("INTEGER")
			node = node.Literal("IntegerLiteral", int(token.value))
		elif self.lookahead.type == "FLOAT":
			token = self._eat("FLOAT")
			node = node.Literal("FloatLiteral", float(token.value))
		elif self.lookahead.type == "STRING":
			token = self._eat("STRING")
			node = node.Literal("StringLiteral", str(token.value)[1: -1])
		elif self.lookahead.type == "true":
			self._eat("true")
			node = node.Literal("BooleanLiteral", True)
		elif self.lookahead.type == "false":
			self._eat("false")
			node = node.Literal("BooleanLiteral", False)
		elif self.lookahead.type == "null":
			self._eat("null")
			node = node.Literal("NullLiteral", None)
		else:  # pragma: no cover
			raise SyntaxError("Literal: unexpected literal production")

		return node
