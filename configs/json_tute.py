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
