from spl_parser.syntax_parser import find_related_trees
from spl_parser.syntax_parser import parse_syntax_tree


class SPLTerm:
    def __init__(self, name, syntax):
        self.name = name
        self.syntax = syntax
        self.description = ""

    def get_bnf_syntax(self):
        return f"<{self.name}> ::= {self.syntax}"


class SPLCommand(SPLTerm):
    def __init__(self, name, syntax):
        super().__init__(name, syntax)
        self.related_trees = dict()
        self.aliases = list()
        self.arguments = list()
        self.functions = list()
        self.operators = list()

    def find_related_trees(self, syntax_trees):
        self.related_trees = find_related_trees(self.name, syntax_trees)

    def parse(self):
        for tree in self.related_trees.values():
            (arguments, functions, operators) = parse_syntax_tree(tree)
            self.arguments.extend(list(arguments))
            self.functions.extend(list(functions))
            self.operators.extend(list(operators))
