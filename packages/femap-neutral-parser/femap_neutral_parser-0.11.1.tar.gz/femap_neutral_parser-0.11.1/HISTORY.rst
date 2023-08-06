History
=======

0.8.3 (2021-09-12)
------------------

Major internal refactoring

* ``output_vectors`` becomes internal (``_output_vectors``). The recommended ways to access data is now ``Parser.vectors()`` or ``Parser.get()`` at a higher level.
* no more ``autotranslate`` initialisation parameter. Everything is harmonized under the hood.


0.6.0 (2021-07-12)
------------------

* add engineering shortcuts
* harmonize NodeID and SubcaseID with ``pynastran``
* vectors are now case insensible


0.5.0 (2021-04-16)
------------------

* improve parsing speed on large files


0.4.0 (2021-04-16)
------------------

add:

* ``Parser.info()``
* ``Parser.vectors()``


0.3.0 (2021-04-16)
------------------

* add ``Parser.info()`` and ``Parser.vectors()``
* update documentation
* add info() ``doprint`` option


0.2.0 - 0.3.0 (2021-04-16)
--------------------------

* Update Documentation


0.1.0 (2021-03-24)
------------------

First release on PyPI.


