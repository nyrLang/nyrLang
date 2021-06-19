import json

from Nyr.Parser import Parser

if __name__ == '__main__':
	inp: str = ""

	with open("input.nyr", "r") as f:
		inp = f.read()

	parser = Parser()
	ast = parser.parse(inp)

	print(json.dumps(ast, indent=2))
