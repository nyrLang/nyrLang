import os

import pytest

from Nyr.Interpreter.Interpreter import Interpreter
from Nyr.Parser.Parser import Parser


@pytest.mark.parametrize(
	("filePath", "expectedEnv"), (
		(os.path.join("..", "examples", "Factorial.nyr"), {"fac1": 1, "fac10": 3628800}),
		(os.path.join("..", "examples", "Fibonacci.nyr"), {"fib1": 1, "fib10": 55}),
		(os.path.join("..", "examples", "Functions.nyr"), {"twoSquared": 4, "tenSquared": 100, "fourCubed": 64}),
		(os.path.join("..", "examples", "Variables.nyr"), {"a": "Hello", "b": "Hello, World!", "x": 10, "y": 7, "z": False}),
	),
)
def testExample(filePath: str, expectedEnv: dict):
	with open(filePath, "r") as f:
		code = f.read()

	ast = Parser().parse(code)
	env = Interpreter(ast).interpret()

	assert env == expectedEnv
