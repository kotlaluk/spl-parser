class SplParserError(Exception):
    pass


class CommandNotFoundError(SplParserError):
    def __init__(self, message):
        super().__init__(f"SPL command not found: {message}")


class ParsingError(SplParserError):
    def __init__(self, message):
        super().__init__(f"Error while parsing {message}")
