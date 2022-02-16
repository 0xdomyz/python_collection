from configparser import ConfigParser

pth = ''

cfg = ConfigParser()
cfg.read(pth)
cfg.get('url',nme)

cfg.add_section('url')
cfg.write(f)
cfg.set('url',nme,n)

