# import modules.sub1.subsub1 as util  # assume application run using python at root of project

#testing
import sys
from pathlib import Path

sys.path.append((Path("C:/Users/yzdom/Projects/python_collection/generics/structure/modules/sub1")).resolve().as_posix())
import subsub1 as util


def func():
    print("sub3.func() called")

    util.func()

func()

import pandas
