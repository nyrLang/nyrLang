from typing import Any

from Nyr.Parser import Node
from Nyr.Parser.Tokenizer import Token
from Nyr.Parser.Tokenizer import Tokenizer


class Parser:
	string: str
	tokenizer: Tokenizer
	lookahead: Token
	tokens: tuple[Token]
	tkIndex: int = 0
	fns: dict[str, dict[str, Any]] = dict()

	def __init__(self):
		self.tokenizer = Tokenizer()

	def __reset(self):
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
	def _checkValidAssignmentTarget(node: Node.Node) -> Node.Node:
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

	def parse(self, string: str) -> Node.Program:
		self.__reset()
		self.string = string.strip()
		self.tokenizer.init(self.string)

		self.tokens = self.tokenizer.getTokens()
		self.lookahead = self.getNextToken()

		if self.lookahead.type == "EOF":
			return Node.Program([])

		return self.Program()

	def Program(self) -> Node.Program:
		return Node.Program(self.StatementList())

	def _eat(self, tokenType: str) -> Token:
		token = self.lookahead

		if token.type == tokenType:
			self.lookahead = self.getNextToken()
			return token

		if not self.hasMoreTokens() is True or token.type == "EOF":
			raise SyntaxError(f'Unexpected end of input, expected "{tokenType}"')

		raise SyntaxError(f'Unexpected token: "{token}", expected: "{tokenType}"')  # pragma: no cover

	def StatementList(self, stopLookahead: Any = None) -> list[Node.Node]:
		statementList: list[Node.Node] = [self.Statement()]

		while self.lookahead.type not in [stopLookahead, "EOF"]:
			statementList.append(self.Statement())

		return statementList

	def Statement(self) -> Node.Node:
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

	def SuperExpression(self) -> Node.SuperExpression:
		""" Super
			: 'super'
			;
		"""

		self._eat("super")

		return Node.SuperExpression()

	def ThisExpression(self) -> Node.ThisExpression:
		""" ThisExpression
			: 'this'
			;
		"""

		self._eat("this")

		return Node.ThisExpression()

	def ClassDeclaration(self) -> Node.ClassDeclaration:
		""" ClassDeclaration
			: 'class' Identifier OptClassExtends BlockStatement
		"""

		self._eat("class")
		id_ = self.Identifier()

		superClass = self.ClassExtends() if self.lookahead.type == ":" else None

		body = self.BlockStatement()

		return Node.ClassDeclaration(id_, superClass, body)

	def ClassExtends(self) -> Node.Identifier:
		""" ClassExtends
			: ':' Identifier
			;
		"""

		self._eat(":")

		name = self.Identifier()

		return name

	def FunctionDeclaration(self) -> Node.FunctionDeclaration:
		""" FunctionDeclaration
			: 'def' Identifier '(' OptFormalParameterList ')' BlockStatement
			;
		"""

		self._eat("def")
		name = self.Identifier()
		self.fns.update({name.name: {}})

		self._eat("(")
		params: list[Node.Node] = self.FormalParameterList() if self.lookahead.type != ")" else []
		self._eat(")")
		self.fns[name.name].update({"args": params})

		body = self.BlockStatement()
		self.fns[name.name].update({"body": body})

		return Node.FunctionDeclaration(name, params, body)

	def FormalParameterList(self) -> list[Node.Node]:
		""" FormalParameterList
			: Identifier
			| FormalParameterList ',' Identifier
			;
		"""

		params: list[Node.Node] = [
			self.Identifier(),
		]

		while self.lookahead.type == ",":
			self._eat(",")
			params.append(self.Identifier())

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
		if self.lookahead.type == "while": return self.WhileStatement()
		elif self.lookahead.type == "do": return self.DoWhileStatement()
		elif self.lookahead.type == "for": return self.ForStatement()
		else:  # pragma: no cover
			raise Exception(f"Unknown IterationStatement {self.lookahead.type}")

	def WhileStatement(self) -> Node.WhileStatement:
		self._eat("while")

		self._eat("(")
		test = self.Expression()
		self._eat(")")

		body = self.Statement()

		return Node.WhileStatement(test=test, body=body)

	def DoWhileStatement(self) -> Node.DoWhileStatement:
		self._eat("do")

		body = self.Statement()

		self._eat("while")
		self._eat("(")
		test = self.Expression()
		self._eat(")")
		self._eat(";")

		return Node.DoWhileStatement(body=body, test=test)

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
		declarations: list[Node.Node] = [
			self.VariableDeclaration(),
		]

		while self.lookahead.type == ",":
			self._eat(",")
			declarations.append(self.VariableDeclaration())

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

	def AssignmentOperator(self) -> Token:
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
		return self.LogicalExpression("BitwiseORExpression", "LOGICAL_AND")

	def BitwiseExpression(self, builderName, operatorToken) -> Node.Node:
		builder = getattr(self, builderName)

		left = builder()

		while self.lookahead.type == operatorToken:
			operator = self._eat(operatorToken).value

			right = builder()

			left = Node.ComplexExpression(
				"BitwiseExpression",
				operator,
				left,
				right,
			)

		return left

	def BitwiseORExpression(self) -> Node.Node:
		return self.BitwiseExpression("BitwiseXORExpression", "BITWISE_OR")

	def BitwiseXORExpression(self) -> Node.Node:
		return self.BitwiseExpression("BitwiseANDExpression", "BITWISE_XOR")

	def BitwiseANDExpression(self) -> Node.Node:
		return self.BitwiseExpression("EqualityExpression", "BITWISE_AND")

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

		if self.lookahead.type == "super":
			return self.CallExpression(self.SuperExpression())

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

		fn = None
		if isinstance(callee, Node.Identifier):
			fn = self.fns.get(callee.name, None)
		callExpression = Node.CallExpression(callee, self.Arguments(), fn)

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
		argumentList: list[Node.Node] = [
			self.AssignmentExpression(),
		]

		while self.lookahead.type == ",":
			self._eat(",")
			argumentList.append(self.AssignmentExpression())

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
		if self.lookahead.type == "ADDITIVE_OPERATOR":
			operator = self._eat("ADDITIVE_OPERATOR").value
		elif self.lookahead.type == "LOGICAL_NOT":
			operator = self._eat("LOGICAL_NOT").value
		else:
			operator = None

		if operator is not None:
			return Node.UnaryExpression(operator, self.UnaryExpression())

		return self.LeftHandSideExpression()

	def PrimaryExpression(self) -> Node.Node:
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

	def ParenthesizedExpression(self) -> Node.Node:
		self._eat("(")
		expression = self.Expression()
		self._eat(")")

		return expression

	def Literal(self) -> Node.Literal:
		if self.lookahead.type == "INTEGER":
			token = self._eat("INTEGER")
			node = Node.Literal("IntegerLiteral", int(token.value))
		elif self.lookahead.type == "FLOAT":
			token = self._eat("FLOAT")
			node = Node.Literal("FloatLiteral", float(token.value))
		elif self.lookahead.type == "STRING":
			token = self._eat("STRING")
			node = Node.Literal("StringLiteral", str(token.value)[1: -1])
		elif self.lookahead.type == "true":
			self._eat("true")
			node = Node.Literal("BooleanLiteral", True)
		elif self.lookahead.type == "false":
			self._eat("false")
			node = Node.Literal("BooleanLiteral", False)
		elif self.lookahead.type == "null":
			self._eat("null")
			node = Node.Literal("NullLiteral", None)
		else:  # pragma: no cover
			raise SyntaxError("Literal: unexpected literal production")

		return node
