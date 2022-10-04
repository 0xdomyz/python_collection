"""
Examples
------------
::

    py layout\argparse_tute\optional.py
    py layout\argparse_tute\optional.py -v
    py layout\argparse_tute\optional.py -v -nv aaa
    py layout\argparse_tute\optional.py -h
"""
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    "-v", "--verbose", help="increase output verbosity", action="store_true"
)
parser.add_argument("-nv", help="nv help")

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    if args.verbose:
        print("verbosity turned on")
