import yaml
from pathlib import Path


def read_yaml(path):
    with open(path) as f:
        return yaml.load(f, yaml.FullLoader)


def yaml_writer(data, path):
    with open(path, "w") as f:
        yaml.dump(data, f)


if __name__ == "__main__":
    path = Path(__file__).parent / "config.yaml"
    path2 = Path(__file__).parent / "config2.yaml"
    y = read_yaml(path)
    print(y)
    [*y]
    {**y}
    yaml_writer(y, path2)
    read_yaml(path2)
