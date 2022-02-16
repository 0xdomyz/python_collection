import yaml
from pathlib import Path

path = Path(__file__).parent / 'files/data.yaml'

def read(path = path):
    with open(path) as f:
        return yaml.load(f, yaml.FullLoader)

if __name__ == '__main__':
    y = read()
    print(y)