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


class SPLCommand:
    def __init__(self, name):
        self.name = name
        self.aliases = list()
        self.arguments = list()
        self.functions = list()
        self.operators = list()

    def add_operators(self, operators):
        for o in operators:
            self.operators.append(o)

    def add_arguments(self, arguments):
        for a in arguments:
            self.arguments.append(a)

    def add_functions(self, functions):
        for f in functions:
            self.functions.append(f)