a = {}
a.a = 1  # AttributeError

a = object()
a.a = 1  # AttributeError


class A:
    pass


a = A()
a.a = 1

# example of using name space
####################################

import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument("--a", type=int, default=1)

args = argparser.parse_args()

print(args.a)

# add a new argument
argparser.add_argument("--b", type=int, default=2)

# give the new argument a value
args = argparser.parse_args(["--b", "3"])

# give the new argument 2 values, the old argument 1 value
args = argparser.parse_args(["--a", "2", "--b", "3", "4"])

print(args.a, args.b)

# give another argument a value
args = argparser.parse_args(["--c", "3"])  # error

print(args.c)

# give a pair to namespace
args.d = True
args.d

# create a new namespace
############################
args = argparse.Namespace(a=1, b=2)

print(args.a, args.b)

# add a argument and value pair to the namespace
args.c = 3

print(args.c)

# test if attribute exists
"a" in args
"c" in args
