from configparser import ConfigParser
from pathlib import Path

pth = Path(__file__).parent / 'files/test'
#pth = Path().parent / 'files/test'

#read msg
nme = 'oc'

cfg = ConfigParser()
url = None
cfg.read(pth)
if cfg.has_option('url',nme):
    url = cfg.get('url',nme)
print(url)

#set msg
msg = 'absdf'
nme = 'oc'

cfg = ConfigParser()
cfg.read(pth)
if not cfg.has_section('url'):
    cfg.add_section('url')
cfg.set('url',nme,msg)
with open(pth,'w') as f:
    cfg.write(f)

pth.unlink()