"""
Examples
--------
:
    python layout\scripts\a_script.py
    python layout\scripts\a_script.py abc
    python layout\scripts\a_script.py abc 123
    python layout\scripts\a_script.py -s abc
"""
from argparse import ArgumentParser
from pathlib import Path
import logging

logging.basicConfig(level=20)

parser = ArgumentParser()
parser.add_argument("input1", help="input1 does nothing")
parser.add_argument("-s", "--special", action="store_true")

def main(input1):
    print(input1)

if __name__ == "__main__":
    args = parser.parse_args()
    
    if args.special:
        print("\n".join(str(i) for i in Path(__file__).parent.iterdir()))
    else:
        main(args.input1)

