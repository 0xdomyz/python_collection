#exmaple
from contextlib import contextmanager

def acquire_resource():
    x = 1
    return x

def release_resource(resource):
    del resource

@contextmanager
def managed_resource(*args, **kwds):
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        release_resource(resource)

with managed_resource() as resource:
    print(resource)

#db
from contextlib import contextmanager
from dwopt import lt

@contextmanager
def temp_db():
    tbl_nme = "tmp_5678"
    lt.iris()
    lt.run(f"create table {tbl_nme} as select 1 as col from iris")

    try:
        yield tbl_nme
    finally:
        lt.drop(tbl_nme)


import logging
logging.basicConfig(level=logging.INFO)

with temp_db() as tbl:
    print(lt.qry(tbl).run())

lt.exist("tmp_5678")

