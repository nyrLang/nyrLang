import argparse
import json

from Nyr.Parser.Node import ComplexEncoder
from Nyr.Parser.Parser import Parser


class Args:
	inputFile: str


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

	args = Args()

	argparser.parse_args(namespace=args)

	# CLI mode (read from stdin)
	if args.inputFile == "<stdin>":
		parser = Parser()
		while True:
			cmd = input("nyr> ")
			if cmd == "exit": exit(0)
			ast = parser.parse(cmd)
			print(json.dumps(ast, cls=ComplexEncoder, indent=2))

	# File mode (read from file given via -f flag)
	elif args.inputFile.endswith(".nyr"):
		with open(args.inputFile, "r") as f:
			text = f.read()

		parser = Parser()
		if not text.strip():
			print("Input file empty!\n")
			argparser.print_help()
		else:
			ast = parser.parse(text)
			print(json.dumps(ast, cls=ComplexEncoder, indent=2))

	# Unknown mode
	else:
		argparser.print_help()
		exit(-1)
