# use python to run R codes via cmd
import os


def run_r(rfile):
    os.system("rscript " + rfile)


r_file_content = """
print("Hello World")
"""


def write_r_file(rfile, content):
    with open(rfile, "w") as f:
        f.write(content)


if __name__ == "__main__":
    rfile = "test.R"
    write_r_file(rfile, r_file_content)
    run_r(rfile)


# use a library to run R codes without cmd
import rpy2.robjects as robjects

# install r on linux:
# sudo apt-get install r-base
