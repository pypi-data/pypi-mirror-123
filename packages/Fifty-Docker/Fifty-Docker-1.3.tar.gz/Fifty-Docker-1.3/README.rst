Fifty-Docker
============

Various command-line tools for working with services in docker.

Usage
^^^^^

.. code:: bash

   Usage: j2 [OPTIONS]

   Options:
     -t, --template PATH         The Jinja template to render
     -o, --output_file PATH      The output location of the rendered template
     -d, --default_context PATH  The default context variables to load (YAML)
     --help         Show this message and exit.

Example
^^^^^^^

.. code:: bash

   j2 -t /config-template.properties.j2 -o /etc/config.properties
