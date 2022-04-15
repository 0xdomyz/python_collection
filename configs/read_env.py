import os


def read_env(variable_name):
    return os.environ.get(variable_name)


if __name__ == "__main__":
    os.environ["test"] = "test"
    os.environ.get("test")
    p = read_env("PATH")
    p.split(";")
