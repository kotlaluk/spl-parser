class SPLTerm:
    def __init__(self, name=None, syntax=None):
        self.name = name
        self.syntax = syntax
        self.aliases = set()

    def get_syntax(self):
        return f"<{self.name}> ::= {self.syntax}"

    def set_syntax(self, syntax):
        splitted = syntax.split(" ::= ")
        if len(splitted) == 2:
            self.name = splitted[0].strip()[1:-1]
            self.syntax = splitted[1].strip()

    def add_alias(self, alias):
        self.aliases.add(alias)
