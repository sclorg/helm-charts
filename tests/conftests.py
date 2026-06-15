import os
import sys

from collections import namedtuple
from pathlib import Path

TEST_DIR = Path(__file__).parent.absolute()

Vars = namedtuple("Vars", ["TEST_DIR"])

VARS = Vars(TEST_DIR=TEST_DIR)
