"""
Examples
------------
::

    py positional.py -h
    py positional.py abcderf 5
    py positional.py "abcde rf" 5

use a windows variable::

    set var=abcde34
    py positional.py %var% 5

    set var="abcde rf"
    py positional.py %var% 5
    py positional.py %var% 6
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
parser.add_argument("number", help="a number", type=float)

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    print(args.echo)
    print(args.number)
