from pathlib import Path

import pytest


@pytest.fixture
def examplesDir() -> Path:
	"""Gets path to examples directory"""
	return Path(__file__).resolve().parent.joinpath("examples")
