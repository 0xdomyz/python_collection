import os

def env_reader(variable_name):
    return os.environ.get(variable_name)

if __name__ == "__main__":
    os.environ['test'] = 'test'
    os.environ.get('test')
    p = env_reader("PATH")
    p.split(";")
