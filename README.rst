Sidomo
======

Simple Docker Module: If you can get your software to work in a docker container, then this module will make it work in Python.
-------------------------------------------------------------------------------------------------------------------------------

How to install:
^^^^^^^^^^^^^^^

.. code:: bash

    pip install -e git+https://github.com/caseyjlaw/sidomo.git#egg=sidomo

How to use:
^^^^^^^^^^^

.. code:: python

    from sidomo import Container

    with Container('ubuntu') as c:
        for output_line in c.run('echo hello world'):
            print(output_line)

.. code:: bash
    dodo echo hello world --image ubuntu

Examples:
^^^^^^^^^

-  hello\_world.py is ‘Hello, World!’ as a module
-  ffmpeg.py fetches audio from a URL and transcodes it to WAV format
-  dodo ("docker do") is like sudo, but for a docker container

Ideas:
^^^^^^

-  Replace leaky glue code
-  Run Erlang from Python
-  Resurrect legacy software for use in a modern environment
-  Make a Python module more portable (the only dependency is Docker
   itself)