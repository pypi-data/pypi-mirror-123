================
driver.interface
================


.. image:: https://img.shields.io/pypi/v/driver.interface.svg
        :target: https://pypi.python.org/pypi/driver.interface


A little module that exports the get_driver function to  import a driver class of a base interface 

* Free software: BSD license


Features
--------

.. code-block:: 

    from driver.interface import get_driver

    object = get_driver(
        module  = "<base module providing the interface>"
        driver  = "<the driver that implements the base module class>",
        class_name = "<the class the object refers to>",
        **driver_params = "<dict of params to pass to the driver>"
        )

Credits
-------

This package was created with `Cookiecutter
<https://github.com/cookiecutter/cookiecutter>`_ and the
`cookiecutter-namespace-template
<https://github.com/veit/cookiecutter-namespace-template>`_ project template.
