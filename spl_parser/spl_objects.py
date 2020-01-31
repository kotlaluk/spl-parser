"""
.. module:: spl_objects

Module spl_objects defines SPLTerm and SPLCommand classes that serve as Python
representations for SPL commands and terms.
"""

from spl_parser.syntax_parser import find_related_trees
from spl_parser.syntax_parser import parse_syntax_tree
from spl_parser.cli_print import log_message, print_kv


class SPLTerm:
    """Object representing a generic SPL term."""
    def __init__(self, name, syntax):
        """
        Args:
            name (str): name of the term
            syntax (str): syntax for the term
        """
        self.name = name
        self.syntax = syntax
        self.description = ""

    def get_bnf_syntax(self):
        """Retrieve Pseudo-BNF syntax from the term representation.

        Returns:
            str: syntax string in Pseudo-BNF format
        """
        return f"<{self.name}> ::= {self.syntax}"

    def print(self):
        """Pretty print the SPL term details to terminal."""
        print()
        print_kv("Name", self.name)
        print_kv("Syntax", self.syntax)
        if self.description:
            print_kv("Description", self.description)


class SPLCommand(SPLTerm):
    """Object representing an SPL command."""
    def __init__(self, name, syntax):
        """
        Args:
            name (str): name of the SPL command
            syntax (str): syntax for the SPL command
        """
        super().__init__(name, syntax)
        self.aliases = list()
        self.arguments = set()
        self.functions = set()
        self.operators = set()

    def parse(self, syntax_trees):
        """Parse full properties of the SPL command from syntax trees.

        Details for the SPL command (its arguments, functions, operators) are
        parsed from syntax trees. The trees related to the processed SPL command
        are chosen from all available trees. If the command cannot be parsed
        correctly, a warning is printed to the terminal.

        Args:
            syntax_trees (dict): dictionary containing pre-built syntax trees
        """
        related_trees = find_related_trees(self.name, syntax_trees)
        if related_trees:
            for tree in related_trees.values():
                (arguments, functions, operators) = parse_syntax_tree(tree)
                self.arguments.update(arguments)
                self.functions.update(functions)
                self.operators.update(operators)
        else:
            log_message("WARNING", f"{self.name} command may not work properly")

    def print(self):
        """Pretty print the SPL command details to terminal."""
        super().print()
        if self.aliases:
            print_kv("Aliases", ' '.join(self.aliases))
