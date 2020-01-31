"""
.. module:: exceptions

Defines specific exceptions used in spl_parser package.
"""

class SplParserError(Exception):
    """Generic exception used with spl_parser package."""
    pass


class CommandNotFoundError(SplParserError):
    """Error signalizing that command could not be retrieved.

    Message should specify name of the command.
    """
    def __init__(self, message):
        super().__init__(f"SPL command not found: {message}")


class ParsingError(SplParserError):
    """Error that occurs during parsing.

    Message can specify a name of the command or file where the parsing error
    occurred.
    """
    def __init__(self, message):
        super().__init__(f"Error while parsing {message}")


class AuthenticationError(SplParserError):
    """Used when there is error in authentication towards a remote Splunk server."""
    def __init__(self):
        super().__init__(f"Authentication towards remote Splunk server failed!")


class ConnectionError(SplParserError):
    """Generic error which occurs in communication with a remote Splunk server."""
    def __init__(self):
        super().__init__(f"Error connecting to the remote Splunk server!")


class InitError(SplParserError):
    """Error occuring during initialization phase.

    Such error can be related to the Pseudo-BNF grammar used for parsing, or a
    tmLanguage template.
    """
    def __init__(self):
        super().__init__(f"Error initializing parser! Check grammar or template definitions...")
