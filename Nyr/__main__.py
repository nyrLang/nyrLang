import argparse
import json

from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Node import ComplexEncoder
from Nyr.Parser.Node import Node
from Nyr.Parser.Parser import Parser


class Args:
	inputFile: str
	output: bool
	interpret: bool
	toSExpr: bool
	printAST: bool


def getAst(string: str):
	return Parser().parse(string)


def printAst(ast_: Node, print_: bool):
	if print_ is True:
		print(json.dumps(ast_, cls=ComplexEncoder, indent=2))


def interpret(ast_: Node, interpreter_: Interpreter = None, env_: Env = None):
	if env_ is None:
		env_ = Env()
	if interpreter_ is None:
		return None
	else:
		_env: Env = interpreter_.interpret(ast_, env_)
		print(f"Env = {json.dumps(_env, indent=2)}")


def outputAST(ast_: Node, doOutput: bool):
	if doOutput:
		with open("./ast.json", "w") as o:
			o.write(json.dumps(ast_, cls=ComplexEncoder, indent=2) + "\n")


if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument(
		"-f", "--file",
		required=False,
		default="<stdin>",
		type=str,
		help="Input file (ending with .nyr)",
		dest="inputFile",
	)
	argparser.add_argument(
		"-i", "--interpret",
		required=False,
		default=False,
		type=bool,
		help="Enable interpreter",
		dest="interpret",
	)
	argparser.add_argument(
		"-o", "--output",
		required=False,
		default=False,
		type=bool,
		help="output AST to ast.json",
		dest="output",
	)
	argparser.add_argument(
		"-p", "--print",
		required=False,
		default=False,
		type=bool,
		help="Wether tp print the AST to terminal",
		dest="printAST",
	)

	args = Args()

	argparser.parse_args(namespace=args)

	parser = Parser()
	interpreter = Interpreter() if args.interpret else None

	printAST: bool = args.printAST

	# CLI mode (read from stdin)
	if args.inputFile == "<stdin>":
		env = Env()
		while True:
			cmd = input("nyr> ")
			if cmd == "exit": exit(0)

			if ";" not in cmd:
				cmd += ";"

			ast = getAst(cmd)

			printAst(ast, printAST)
			outputAST(ast, args.output)
			interpret(ast, interpreter, env)

	# File mode (read from file given via -f flag)
	elif args.inputFile.endswith(".nyr"):
		with open(args.inputFile, "r") as f:
			text = f.read()

		if not text.strip():
			print("\n[!] Input file empty!\n")
			argparser.print_help()
		else:
			ast = getAst(text)

			printAst(ast, printAST)
			outputAST(ast, args.output)
			interpret(ast, interpreter)

	# Unknown mode
	else:
		argparser.print_help()
		exit(-1)
