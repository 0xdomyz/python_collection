# example of using importlib
##########################################
import importlib

os = importlib.import_module("os")
type(os)

# import from a path to a module
importlib.import_module("os.path")

# reload a module
importlib.reload(os)

# import a module from a package
importlib.import_module("os.path", "os")

# import a module from a system path to a script
importlib.import_module("os.path", "/usr/lib/python3.9")

# import a function a script
##########################################
from pathlib import Path

path = Path(".") / "layout" / "importlib_tute_module.py"

spec = importlib.util.spec_from_file_location("importlib_tute_module", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

module.func()

# use __import__ to import a module
##########################################
__import__("os")

# append a path to the system path
import sys
from pathlib import Path

path = (Path(".") / "layout").resolve().as_posix()
sys.path.append(path)

import importlib_tute_module

importlib_tute_module.func()
