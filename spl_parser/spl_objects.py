from spl_parser.syntax_parser import find_related_trees
from spl_parser.syntax_parser import parse_syntax_tree
from spl_parser.cli_print import log_message, print_kv


class SPLTerm:
    def __init__(self, name, syntax):
        self.name = name
        self.syntax = syntax
        self.description = ""

    def get_bnf_syntax(self):
        return f"<{self.name}> ::= {self.syntax}"

    def print(self):
        print()
        print_kv("Name", self.name)
        print_kv("Syntax", self.syntax)
        if self.description:
            print_kv("Description", self.description)


class SPLCommand(SPLTerm):
    def __init__(self, name, syntax):
        super().__init__(name, syntax)
        self.aliases = list()
        self.arguments = list()
        self.functions = list()
        self.operators = list()

    def parse(self, syntax_trees):
        related_trees = find_related_trees(self.name, syntax_trees)
        if related_trees:
            for tree in related_trees.values():
                (arguments, functions, operators) = parse_syntax_tree(tree)
                self.arguments.extend(list(arguments))
                self.functions.extend(list(functions))
                self.operators.extend(list(operators))
        else:
            log_message("WARNING", f"{self.name} command may not work properly")

    def print(self):
        super().print()
        if self.aliases:
            print_kv("Aliases", ' '.join(self.aliases))
