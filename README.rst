SPL Parser
==========

SPL Parser is a command-line application for parsing of Splunk’s Search
Processing Language (SPL). The main feature of SPL Parser is the ability to
generate a tmLanguage grammar for SPL, which can be used in various text editors
for syntax highlighting of SPL. SPL Parser is also able to interactively view
details about any SPL command.

Features
--------

- Generate tmLanguage grammar for SPL that can be used for syntax highlighting
- View details about any SPL command
- Use a remote Splunk server or local files

Installation
------------

The project can be installed using pip from TestPyPI::

    pip install --extra-index-url https://test.pypi.org/pypi spl_parser

Or by cloning GitHub repository::

    git clone https://github.com/kotlaluk/spl-parser

and running::

    python setup.py install

Usage
-----

The SPL Parser CLI application can be invoked by running ``spl_parser``.
To view help run::

    spl_parser --help

SPL Parser can work either with a **remote** Splunk server or a **local**
searchbnf file. The remote server is specified by URL, the local file by its
name and path. Note that the local searchbnf file must be in ``.conf`` or
``.json`` format.

If case of a **remote** Splunk server, the user will be prompted for providing
credentials for authentication. Alternatively, these credentials can be provided
by setting ``SPLUNK_USERNAME`` and ``SPLUNK_PASSWORD`` environment variables.

In both cases, the application allows to **view** details about a particlular
SPL command or **generate** a tmLanguage grammar file.

f using **view** command, the command name is expected as argument. The command
details are then retrieved and displayed in the console.

Example of **view** invocation in **remote** mode::

    spl_parser remote https://localhost:8089 view transaction

If using **generate** command, a tmLanguage grammar will be generated and saved
in the file ``spl.tmLanguage.json``. Alternatively, a file name can be specified
by using ``--outfile`` option. The generated grammar file can then be used
with a text editor for syntax highlighting of SPL.

Example **generate** invocation in **local** mode::

    spl_parser local examples/searchbnf.conf generate

Syntax highlighting
-------------------

This repository contains a prepared extension for VSCode text editor. All you
need is to copy the generated grammar file ``spl.tmLanguage.json`` into the
folder of the extension ``spl-highlighter/syntaxes``, and copy the extension
folder into your installation of VSCode (typically ``~/.vscode/extensions``).

New files with ``.spl`` file extension will automatically provide syntax
highlighting for Splunk queries. The extension allows also to set "SPL Theme"
with colors similar to those in Splunk Web interface.

Testing
-------

The project contains a bundle of tests.

These can be invoked by running::

    python setup.py test

Documentation
-------------

Documentation of the project is available at
`Read the Docs <https://spl_parser.readthedocs.io>`_.

To build the documentation manually::

   cd docs
   make html

and open the file ``docs/_build/html/index.html`` in a web browser.

Author
------

Lukáš Kotlaba (lukas.kotlaba@gmail.com)

License
-------

The project is licensed under GNU General Public License v3.0.
