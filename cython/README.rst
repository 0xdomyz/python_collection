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