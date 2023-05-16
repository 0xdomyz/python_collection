"""
::

    python3.9 setup.py build_ext --inplace

    python3.9 run.py

    # html report
    cython -a integrate_cy.pyx
    cython -a integrate_cy_cdef.pyx
    cython -a integrate_cy_naive.pyx

    explorer.exe integrate_cy.html
    explorer.exe integrate_cy_cdef.html
    explorer.exe integrate_cy_naive.html

"""

import time

from integrate import integrate_f
from integrate_cy import integrate_f as integrate_f_cy
from integrate_cy_cdef import integrate_f as integrate_f_cy_cdef
from integrate_cy_naive import integrate_f as integrate_f_cy_naive

if __name__ == "__main__":
    args = (1, 2, 20000000)

    t = time.time()
    integrate_f(*args)
    print(f"{time.time()-t = }")

    t = time.time()
    integrate_f_cy_naive(*args)
    print(f"{time.time()-t = }")

    t = time.time()
    integrate_f_cy(*args)
    print(f"{time.time()-t = }")

    t = time.time()
    integrate_f_cy_cdef(*args)
    print(f"{time.time()-t = }")
