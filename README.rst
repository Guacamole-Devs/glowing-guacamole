guacamole
======

Install
-------

Run Setup Script::
    > .\setup.ps1
-> IF Flask is not install (Error) run 
Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install guacamole::

    $ pip install -e .

Or if you are using the master branch, install Flask from source before
installing guacamole::

    $ pip install -e ../..
    $ pip install -e .

Run
---

::

    $ export FLASK_APP=guacamole
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run

Or on Windows cmd::

    > set FLASK_APP=guacamole
    > $env:FLASK_ENV=development
    > flask init-db
    > flask run

Open http://127.0.0.1:5000 in a browser.


Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
