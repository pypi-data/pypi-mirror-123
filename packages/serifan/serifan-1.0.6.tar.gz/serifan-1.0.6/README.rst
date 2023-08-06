=======
Serifan
=======

.. image:: https://img.shields.io/pypi/v/serifan.svg?logo=PyPI&label=Version&style=flat-square   :alt: PyPI
    :target: https://pypi.org/project/serifan

.. image:: https://img.shields.io/pypi/pyversions/serifan.svg?logo=Python&label=Python-Versions&style=flat-square
    :target: https://pypi.org/project/serifan

.. image:: https://img.shields.io/github/license/bpepple/serifan
    :target: https://opensource.org/licenses/GPL-3.0  

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Quick Description
-----------------
A python wrapper for the shortboxed.com_ API.

.. _shortboxed.com: https://shortboxed.com/

Installation
------------

PyPi
~~~~

.. code:: bash

  $ pip3 install --user serifan

Example Usage
-------------
.. code-block:: python

    import serifan

    m = serifan.api()

    # Get this weeks comic releases.
    results = m.new_releases()

    # Print the results
    for i in results:
        print(f"{i.title}")

Documentation
-------------
- `Read the project documentation <https://serifan.readthedocs.io/en/latest/>`_
 
Bugs/Requests
-------------
  
Please use the `GitHub issue tracker <https://github.com/bpepple/serifan/issues>`_ to submit bugs or request features.

License
-------

This project is licensed under the `GPLv3 License <LICENSE>`_.
