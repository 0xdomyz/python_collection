"""
Examples
------------
::

    python combined.py   
    usage: combined.py [-h] [-v] square
    combined.py: error: the following arguments are required: square

    python combined.py 3
    9

    python combined.py 3 -v
    3^2 == 9

    python combined.py 3 -vv
    the square of 3 equals 9
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count", default=0,
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbosity >= 2:
    print(f"the square of {args.square} equals {answer}")
elif args.verbosity >= 1:
    print(f"{args.square}^2 == {answer}")
else:
    print(answer)