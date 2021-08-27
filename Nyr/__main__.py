import argparse
import json
import sys
from pprint import pp

from Nyr.Interpreter.Env import Env
from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Node import ComplexEncoder
from Nyr.Parser.Node import Node
from Nyr.Parser.Parser import Parser


class Args:
	inputFile: str
	output: bool
	interpret: bool
	printAST: bool


def getAst(string: str):
	return Parser().parse(string)


def printAst(ast_: Node, print_: bool):
	if print_ is True:
		print(json.dumps(ast_, cls=ComplexEncoder, indent=2))


def interpret(ast_: Node, interpret_: bool, env_: Env = None):
	if env_ is None:
		env_ = Env()
	if interpret_ is True:
		_env: Env = Interpreter(ast_).interpret()
		print(f"Env = ", end="")
		pp(_env)


def outputAST(ast_: Node, doOutput: bool):
	if doOutput:
		with open("./ast.json", "w") as o:
			o.write(json.dumps(ast_, cls=ComplexEncoder, indent=2) + "\n")


if __name__ == "__main__":
	if (sys.version_info.major, sys.version_info.minor) < (3, 9):
		print(f"At least python 3.9 is required to run this code. Your version is: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
		exit(1)
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

	printAST: bool = args.printAST

	# CLI mode (read from stdin)
	if args.inputFile == "<stdin>":
		env = Env()
		while True:
			cmd = input("nyr> ")
			if cmd == "exit": exit(0)
			elif cmd == "clear":
				print("\033c", end="")
				continue

			if ";" not in cmd:
				cmd += ";"

			ast = getAst(cmd)

			printAst(ast, printAST)
			outputAST(ast, args.output)
			interpret(ast, args.interpret, env)

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
			interpret(ast, args.interpret)

	# Unknown mode
	else:
		argparser.print_help()
		exit(-1)
