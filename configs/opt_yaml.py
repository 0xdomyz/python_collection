import yaml
from pathlib import Path

path = Path(__file__).parent / 'config.yaml'

def yaml_reader(path):
    with open(path) as f:
        return yaml.load(f, yaml.FullLoader)

if __name__ == '__main__':
    y = yaml_reader(path)
    print(y)
    [*y]
    {**y}