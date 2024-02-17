"""
Examples
------------
::

    py layout\argparse_tute\combined.py  
    py layout\argparse_tute\combined.py 3
    py layout\argparse_tute\combined.py 3 -o 876
    py layout\argparse_tute\combined.py 3 -v
    py layout\argparse_tute\combined.py 3 -vv
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument("-o", help="optional value")
parser.add_argument(
    "-v", "--verbosity", action="count", default=0, help="increase output verbosity"
)

if __name__ == "__main__":
    args = parser.parse_args()
    answer = args.square**2

    print(args.o)

    if args.verbosity >= 2:
        print(f"the square of {args.square} equals {answer}")
    elif args.verbosity >= 1:
        print(f"{args.square}^2 == {answer}")
    else:
        print(answer)
