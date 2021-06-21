from Nyr.Node import Node
from Nyr.Parser import Parser


def testMultipleStrings():
	parser = Parser()
	ast = parser.parse("'Hello'; '42';")

	body = ast["body"]
	assert len(body) == 2

	expression = body[0]["expression"]
	assert expression["type"] == Node.StringLiteral
	assert expression["value"] == "Hello"

	expression = body[1]["expression"]
	assert expression["type"] == Node.StringLiteral
	assert expression["value"] == "42"


def testMutlipleNumbers():
	parser = Parser()
	ast = parser.parse("1; 163543516;")

	body = ast["body"]
	assert len(body) == 2

	expression = body[0]["expression"]
	assert expression["type"] == Node.IntegerLiteral
	assert expression["value"] == 1

	expression = body[1]["expression"]
	assert expression["type"] == Node.IntegerLiteral
	assert expression["value"] == 163543516


def testMultipleFloats():
	parser = Parser()
	ast = parser.parse("3.141; 2.718;")

	body = ast["body"]
	assert len(body) == 2

	expression = body[0]["expression"]
	assert expression["type"] == Node.FloatLiteral
	assert expression["value"] == 3.141

	expression = body[1]["expression"]
	assert expression["type"] == Node.FloatLiteral
	assert expression["value"] == 2.718


def testMixed():
	parser = Parser()
	ast = parser.parse("'Hello'; 42; 3.141;")

	body = ast["body"]
	assert len(body) == 3

	expression = body[0]["expression"]
	assert expression["type"] == Node.StringLiteral
	assert expression["value"] == "Hello"

	expression = body[1]["expression"]
	assert expression["type"] == Node.IntegerLiteral
	assert expression["value"] == 42

	expression = body[2]["expression"]
	assert expression["type"] == Node.FloatLiteral
	assert expression["value"] == 3.141
