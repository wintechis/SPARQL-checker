# TODO

import subprocess
import sys
import importlib

from config import PACKAGES

for package in PACKAGES:
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        importlib.import_module(package)
