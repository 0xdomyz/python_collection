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


#db from decorator
import functools
from contextlib import contextmanager
import nanoid
from dwopt import lt
import time

def temp_table_name()->str:
    while True:
        name = "temp_" + nanoid.generate("0123456789abcdefghijklmnopqrstuvwxyz", 8)
        if not lt.exist(name):
            break
        else:
            time.sleep(1)
    return name


def temp_table(db):
    """
    Require kwargs temp to be True. 

    Function to return a sql str. 
    """
    def decorate(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            if "temp" in kwargs and kwargs["temp"]:
                @contextmanager
                def func_as_contextmanager(*args, **kwargs):
                    name = temp_table_name()
                    try:
                        sql = func(*args, **kwargs)
                        db.run(f"create table {name} as {sql}")
                        yield name
                    finally:
                        db.drop(name)
                result = func_as_contextmanager(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            return result
        return new_func
    return decorate

class A:

    def __init__(self):
        pass

    @temp_table(db=lt)
    def func(self, x, temp=False):
        """
        Examples
        ----------------
        ::

            import logging
            logging.basicConfig(level=logging.INFO)

            a = A()
            print(a.func.__doc__)

            lt.iris()
            a.func(1)
            with a.func(1, temp=True) as tbl:
                print(tbl)
                lt.qry(tbl).run()

            lt.qry(tbl).run()
        """
        return f"select {x} as col from iris"
