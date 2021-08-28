import os
from pathlib import Path

import pytest


@pytest.fixture
def examplesDir():
	examplesDir = Path(__file__).resolve().parent.joinpath(os.path.join(".", "examples"))
	os.makedirs(examplesDir, exist_ok=True)
	return examplesDir
