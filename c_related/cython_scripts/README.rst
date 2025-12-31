Installation
-----------------

.. code-block:: console

    pip install Cython
    pip install --upgrade setuptools

Usage
------------

Setup tool:

.. code-block:: console

    python3.9 setup.py build_ext --inplace

Jupyter::

    %load_ext Cython
    %%cython --annotate

New examples
-----------------

- ``scientific_examples/``: finite-difference diffusion step using typed memoryviews and tight loops. Benchmarked against pure Python.
- ``app_examples/``: byte-level log parsing (count delimiters, extract fields) to show how Cython speeds up everyday text handling.