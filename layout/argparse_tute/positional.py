"""
Examples
------------
::

    python positional.py
    usage: positional.py [-h] echo
    positional.py: error: the following arguments are required: echo

    python positional.py ert
    ert
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)