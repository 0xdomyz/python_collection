"""
Examples
------------
::

    py layout\argparse_tute\positional.py
    py layout\argparse_tute\positional.py 1 5
    py layout\argparse_tute\positional.py -h
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
parser.add_argument("number", help="a number",type=float)

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    print(args.echo)
    print(args.number)