from typing import Sequence

from nyr.v2.tokenizer import Token


MAXITERATIONS = 2 ** 16
MAXRECURSIONDEPTH = 128


def interpret(tokenStream: Sequence[Token]):
	...
