Usage
=====

SPL Parser is used as a CLI application. After installation of the package,
the interface can be invoked by calling ``spl_parser``.

SPL Parser offers following options (can be viewed by calling ``spl_parser --help``):

.. code-block:: console

    Usage: spl_parser [OPTIONS] COMMAND [ARGS]...

        Tool for processing Splunk's Search Processing Language (SPL).

    Options:
    --debug  Enable debug output.
    --help   Show this message and exit.

    Commands:
    local   Specify local searchbnf file (.json or .conf) as SOURCE_FILE.
    remote  Specify URL of a remote Splunk server.

SPL Parser can work either with a **remote** Splunk server or a **local**
searchbnf file. The remote server is specified by URL, the local file by its
name and path. Note that the local searchbnf file must be in ``.conf`` or
``.json`` format.

After specifying a **local** resource, the following options are available:

.. code-block:: console

   Usage: spl_parser local [OPTIONS] SOURCE_FILE COMMAND [ARGS]...

     Specify local searchbnf file (.json or .conf) as SOURCE_FILE.

   Options:
    --help  Show this message and exit.

   Commands:
    generate  Generate a tmLanguage grammar for SPL.
    view      View details about an SPL command.

After specifying a **remote** resource, the following options are available:

.. code-block:: console

    Usage: spl_parser remote [OPTIONS] URL COMMAND [ARGS]...

        Specify URL of a remote Splunk server.

    Options:
     --help           Show this message and exit.

    Commands:
     generate  Generate a tmLanguage grammar for SPL.
     view      View details about an SPL command.

If case of a **remote** Splunk server, the user will be prompted for providing
credentials for authentication. Alternatively, these credentials can be provided
by setting ``SPLUNK_USERNAME`` and ``SPLUNK_PASSWORD`` environment variables.

In both cases, the application allows to **view** details about a particlular
SPL command or **generate** a tmLanguage grammar file.

If using **view** command, the command name is expected as argument. The command
details are then retrieved and displayed in the console.

If using **generate** command, a tmLanguage grammar will be generated and saved
in the file ``spl.tmLanguage.json``. Alternatively, a file name can be specified
by using ``--outfile`` option. The generated grammar file can then be used
with a text editor for syntax highlighting of SPL.
