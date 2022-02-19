import warnings
from contextlib import redirect_stdout
import io

with redirect_stdout(io.StringIO()) as f:
    help(pow)
s = f.getvalue()