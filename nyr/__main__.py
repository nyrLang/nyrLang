import argparse
import json
import sys
from pprint import pp

from nyr.interpreter.interpreter import Interpreter
from nyr.parser.node import ComplexEncoder
from nyr.parser.node import Program
from nyr.parser.parser import Parser


class Args:
	inputFile: str
	output: bool
	interpret: bool
	printAST: bool
	debug: bool


def getAst(string: str) -> Program:
	return Parser().parse(string)


def printAst(ast_: Program):
	if args.printAST:
		print(json.dumps(ast_, cls=ComplexEncoder, indent=2))


def interpret(ast_: Program):
	if args.interpret:
		_env = Interpreter(args.debug).interpret(ast_)
		print(f"Env = ", end="")
		pp(_env)


def outputAST(ast_: Program):
	if args.output:
		with open("./ast.json", "w") as o:
			o.write(json.dumps(ast_, cls=ComplexEncoder, indent=2) + "\n")


args = Args()


def main() -> int:
	if sys.version_info < (3, 9):
		print(f"At least python 3.9 is required to run this code. Your version is: {sys.version_info}")
		return 1
	argparser = argparse.ArgumentParser()
	argparser.add_argument(
		"-f", "--file",
		default="<stdin>",
		type=str,
		help="Input file (ending with .nyr)",
		dest="inputFile",
	)
	argparser.add_argument(
		"-i", "--interpret",
		action="store_false",
		help="Disable interpreter",
		dest="interpret",
	)
	argparser.add_argument(
		"-o", "--output",
		action="store_true",
		help="Output AST to ast.json",
		dest="output",
	)
	argparser.add_argument(
		"-p", "--print",
		action="store_true",
		help="Wether to print the AST to terminal",
		dest="printAST",
	)
	argparser.add_argument(
		"-d", "--debug",
		action="store_true",
		help="Wether to print debug messages on what the interpreter is doing",
		dest="debug",
	)

	argparser.parse_args(namespace=args)

	# REPL (read from stdin)
	if args.inputFile == "<stdin>":
		while True:
			try:
				cmd = input("nyr> ")
			except KeyboardInterrupt:
				return 0
			except EOFError:
				return 0
			except Exception:
				raise

			if cmd == "exit": return 0
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
		return -1


if __name__ == "__main__":
	raise SystemExit(main())
