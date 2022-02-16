"""https://docs.python.org/3/library/pathlib.html"""
from pathlib import Path

f = __file__

p = Path(f).parent

Path(__file__).parents[2]

ap = p.resolve().as_posix()
ap

for i in p.iterdir():
    print(i)

for i in p.iterdir():
    if i.isdir():
        print(i)

(p / 'files').resolve()

(p / 'files').exists()

(p / 'file').exists()

with open(p / 'files/data.yml') as f:
    print(f)

for i in p.glob('*.py'):
    print(i)

for i in p.glob('*/*.py'):
    print(i)

for i in p.glob('**/*.yml'):
    print(i)

p.home()

(p.home() / '.dwopt').resolve()

p.home().joinpath('.dwopt').resolve()

[i for i in p.glob('files/*.yml')]

[i for i in p.glob('files/*ta.yml')]

q = p.joinpath('paths.py')
aq = q.resolve().as_posix()
aq

q.stem

q.suffix

q.name

q.with_name('read_env.py')


""""""
import os

os.path.abspath('')

os.path.abspath('../files/data.yml')

os.path.dirname(aq)

with open(os.path.join(ap,'files','data.yml')) as f: print(f)


"""https://docs.python.org/3/library/glob.html"""
from glob import glob

glob(ap+'/**/*.yml')


""""""
import sys

sys.path

sys.path.insert(0,p)


""""""
if __name__ == '__main__':
    path = Path(__file__).parent / 'files/data.yml'
    print(path)