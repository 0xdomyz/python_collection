# cython: boundscheck=False
# cython: wraparound=False
# cython: language_level=3
# cython: nonecheck=False

import cython


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t count_char(bytes data, unsigned char target):
    """Count how many times *target* byte appears in *data*."""
    cdef Py_ssize_t i, n = len(data)
    cdef Py_ssize_t count = 0
    cdef const unsigned char *buf = data
    for i in range(n):
        if buf[i] == target:
            count += 1
    return count


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t count_fields(bytes line, unsigned char sep=44):
    """Count CSV-like fields by counting separators (default comma)."""
    return count_char(line, sep) + 1 if line else 0


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef tuple split_first(bytes line, unsigned char sep=44):
    """Split at first separator, returning (head, tail)."""
    cdef Py_ssize_t i, n = len(line)
    cdef const unsigned char *buf = line
    for i in range(n):
        if buf[i] == sep:
            return line[:i], line[i + 1 :]
    return line, b""
