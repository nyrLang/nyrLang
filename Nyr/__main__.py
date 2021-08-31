import argparse
import json
import sys
from enum import Enum
from pprint import pp

from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Node import ComplexEncoder
from Nyr.Parser.Node import Program
from Nyr.Parser.Parser import Parser


class Args:
	inputFile: str
	output: int
	interpret: int
	printAST: int


class EArgs(Enum):
	output = 0b0001
	interpret = 0b0010
	printAST = 0b0100


def getAst(string: str) -> Program:
	return Parser().parse(string)


def printAst(ast_: Program):
	if args.printAST & EArgs.printAST.value == EArgs.printAST.value:
		print(json.dumps(ast_, cls=ComplexEncoder, indent=2))


def interpret(ast_: Program):
	if args.interpret & EArgs.interpret.value == EArgs.interpret.value:
		_env = Interpreter(ast_).interpret()
		print(f"Env = ", end="")
		pp(_env)


def outputAST(ast_: Program):
	if args.output & EArgs.output.value == EArgs.output.value:
		with open("./ast.json", "w") as o:
			o.write(json.dumps(ast_, cls=ComplexEncoder, indent=2) + "\n")


args = Args()

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
		action="store_const",
		const=0,
		default=EArgs.interpret.value,
		help="Enable interpreter",
		dest="interpret",
	)
	argparser.add_argument(
		"-o", "--output",
		required=False,
		action="store_const",
		const=EArgs.output.value,
		default=0,
		help="output AST to ast.json",
		dest="output",
	)
	argparser.add_argument(
		"-p", "--print",
		required=False,
		action="store_const",
		const=EArgs.printAST.value,
		default=0,
		help="Wether tp print the AST to terminal",
		dest="printAST",
	)

	argparser.parse_args(namespace=args)

	parser = Parser()

	# CLI mode (read from stdin)
	if args.inputFile == "<stdin>":
		while True:
			cmd = input("nyr> ")
			if cmd == "exit": exit(0)
			elif cmd == "clear":
				print("\033c", end="")
				continue

			if ";" not in cmd:
				cmd += ";"

			ast = getAst(cmd)

			printAst(ast)
			outputAST(ast)
			interpret(ast)

	# File mode (read from file given via -f flag)
	elif args.inputFile.endswith(".nyr"):
		with open(args.inputFile, "r") as f:
			text = f.read()

		if not text.strip():
			print("\n[!] Input file empty!\n")
			argparser.print_help()
		else:
			ast = getAst(text)

			printAst(ast)
			outputAST(ast)
			interpret(ast)

	# Unknown mode
	else:
		argparser.print_help()
		exit(-1)
