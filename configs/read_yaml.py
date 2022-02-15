import yaml

def read_config():
    path = ''
    with open(path) as f:
        return yaml.load(f, yaml.FullLoader)

if __name__ == '__main__':
    read_config()