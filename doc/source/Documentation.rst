Documentation
=============
Every developer likes to have documentation, but no one really likes to write it.

Sphinx and rst
--------------
To help us with the documentation proces, CodeKlavier uses the Sphinx package that converts rst-files (that are easy to write) to html-files that are beautiful and easy to browse. On top of that: Sphinx can 'walk' over the python source code and generate the documentation out of the docstrings in the python code.

Rst-files are plain text files with some basic formatting. You can underline words with === to indicate a header and you use '*' to use **boldface** and so on. There is enough material on the internet to help you with the basics.

Installation
............
You can use ``pip3`` to install the Sphinx-package by running::

  pip3 install sphinx

Use pip3 because CodeKlavier uses python **3** and not python 2.

.. NOTE::
  If you used the ``requirements.txt`` file to install CodeKlavier, you have already installed Sphinx.

Setup
.....
The ``doc`` folder was created to put everything that deals with documentation. From that directory we made the setup by running ``sphynx-quickstart`` and answering the questions that pop up. This creates the ``source`` and ``build`` directories and provides you with a ``Makefile`` file. Some small tweaks to the ``source/conf.py`` were made to finalise the installation.

Sphinx can autogenerate some documentation based on the docstrings from the python code. Make sure you enable the "autodoc" module in the ``conf.py`` file and the you insert the correct "path". With the command: ``sphinx-apidoc -o <output-path> module-path`` you can include an entire package/module in one go and it generates and ``.rst`` file that you can include in the ``modules.rst`` file.

How to write documentation
--------------------------
Change existing rst-files, or create additional files in case you want to create a new page.

For documeting the python code: please add appropiate docstring in the code itself.

How to build the documentation
------------------------------
Most likely, you'll want to build towards html-code. You can make a build by running ``make html`` from the ``doc`` folder. This will run sphinx in html-mode and save an updated version of the html in the ``doc/build`` directory.
