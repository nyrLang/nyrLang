import os

import pytest

from nyr.interpreter.interpreter import Interpreter
from nyr.parser.parser import Parser


@pytest.mark.parametrize(
	("fileName", "expectedEnv"), (
		pytest.param(
			"Factorial.nyr",
			{"fac1": 1, "fac10": 3628800},
			id="Factorial.nyr",
		),
		pytest.param(
			"Fibonacci.nyr",
			{"fib1": 1, "fib10": 55},
			id="Fibonacci.nyr",
		),
		pytest.param(
			"Functions.nyr",
			{"twoSquared": 4, "tenSquared": 100, "fourCubed": 64},
			id="Functions.nyr",
		),
		pytest.param(
			"Variables.nyr",
			{"a": "Hello", "b": "Hello, World!", "x": 10, "y": 7, "z": False},
			id="Variables.nyr",
		),
	),
)
@pytest.mark.usefixtures("examplesDir")
@pytest.mark.xfail(reason="print function not available in python interpreter")
def testExample(examplesDir: str, fileName: str, expectedEnv: dict):
	with open(os.path.join(examplesDir, fileName), "r") as f:
		code = f.read()

	ast = Parser().parse(code)
	env = Interpreter().interpret(ast)

	assert env == expectedEnv
