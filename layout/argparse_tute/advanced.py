"""
Examples
------------
::

    python advanced.py      
    usage: advanced.py [-h] [-v | -q] x y
    advanced.py: error: the following arguments are required: x, y

    python advanced.py 2 3
    2^3 == 8

    python advanced.py 2 3 -v
    2 to the power 3 equals 8

    python advanced.py 2 3 -q
    8
"""
import argparse

parser = argparse.ArgumentParser(description="calculate X to the power of Y")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))
