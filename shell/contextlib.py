from contextlib import redirect_stdout
import io

if __name__ == "__main__":
    with redirect_stdout(io.StringIO()) as f:
        help(pow)
    s = f.getvalue()
    print(s)
