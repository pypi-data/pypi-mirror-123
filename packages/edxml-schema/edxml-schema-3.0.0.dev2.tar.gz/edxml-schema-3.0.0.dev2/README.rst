|license| |pyversion|

.. |license| image::  https://img.shields.io/badge/License-CC%20BY--ND%203.0-lightgrey.svg
.. |pyversion| image::  https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue

===============================
The EDXML Schema Python Package
===============================

This is a Python package that provides the EDXML RelaxNG schema. It can be used to include the schema in Python projects by adding this package as a dependency.

Besides the actual schema the package also provides a constant which contains the path to the schema. It can be imported like this::

    from edxml_schema import SCHEMA_PATH

