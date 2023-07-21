# from tutorial
#####################
import json

# list, dict, str, int, float, True, False, None, tuple
json.dumps(["foo", {"bar": ("baz", None, 1.0, 2)}])

json.dumps([1, 2, 3])
json.dumps((1, 2, 3))  # no difference between tuple and list

print(json.dumps('"foo\bar'))

print(json.dumps("\u1234"))

print(json.dumps("\\"))

# sort
print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))

# stream
from io import StringIO

io = StringIO()
json.dump(["streaming API"], io)
io.getvalue()

# compact
import json

json.dumps([1, 2, 3, {"4": 5, "6": 7}])
json.dumps([1, 2, 3, {"4": 5, "6": 7}], separators=(",", ":"))  # get rid of space

# pretty
import json

print(json.dumps({"4": 5, "6": 7}, sort_keys=True))
json.dumps({"4": 5, "6": 7}, sort_keys=True, indent=4)
print(json.dumps({"4": 5, "6": 7}, sort_keys=True, indent=4))  # spaces and \n

# decode
import json

json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')

json.loads('"\\"foo\\bar"')

from io import StringIO

io = StringIO('["streaming API"]')
json.load(io)


# specialize
import json


def as_complex(dct):
    if "__complex__" in dct:
        return complex(dct["real"], dct["imag"])
    return dct


json.loads('{"__complex__": true, "real": 1, "imag": 2}')
json.loads('{"__complex__": true, "real": 1, "imag": 2}', object_hook=as_complex)

import decimal

json.loads("1.1", parse_float=decimal.Decimal)


# some custom funcs
############################

# example of save and load json file of list of dict
import json
from pathlib import Path


def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    pth = Path(__file__).parent / "test.json"
    data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}, "asdf", 567, 12.8]
    save_json(data, pth)
    load_json(pth)
    # pth.unlink()
