class SPLTerm:
    def __init__(self, name, syntax):
        self.name = name
        self.syntax = syntax
        self.aliases = set()

    def get_syntax(self):
        return f"<{self.name}> ::= {self.syntax}"

    def add_alias(self, alias):
        self.aliases.add(alias)
