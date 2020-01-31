"""
.. module:: syntax_parser

This module defines the core functions responsible for the parsing of Pseudo-BnF
grammar, building syntax trees from it and manipulating with them.
"""

from lark import Lark
from lark.exceptions import GrammarError, UnexpectedCharacters, UnexpectedEOF

from spl_parser.cli_print import log_message
from spl_parser.exceptions import InitError


class LarkParser:
    """Class serving as a simple wrapper for Lark."""
    def __init__(self, grammar):
        """
        Args:
            grammar (str): loaded contents of the file defining Lark grammar\
            for Pseudo-BNF.
        """
        self.__parser =  Lark(grammar, parser="earley")

    def parse(self, expression):
        """Parse a Pseudo-BNF expression using Lark.

        Args:
            expression (str): a Pseudo-BNF expression to parse

        Returns:
            lark.Tree: created syntax tree
        """
        return self.__parser.parse(expression)


def choose_trees(names, trees):
    """Choose syntax trees based on their names.

    Args:
        names (list): names of the trees to choose.
        trees (dict): group of available syntax trees

    Returns:
        dict: a copy of tree dict containing only trees, whose names were\
        present in the list
    """
    chosen = dict()
    for name in names:
        try:
            chosen[name] = trees[name]
        except KeyError:
            pass
    return chosen


def get_token_data(subtree):
    """Get data from the leaf of a subtree.

    Args:
        subtree (lark.Tree): [description]

    Returns:
        str: String representation of the data contained in the first leaf of\
        the subtree.
    """
    return str(subtree.children[0])


def build_syntax_trees(pseudo_bnf, spl_terms):
    """Build syntax trees from Pseudo-BNF definitions.

    Provided SPLTerm objects should contain Pseudo-PNF definition of the syntax.
    This function builds syntax trees from the syntax definitions, based on
    the provided Lark grammar.

    Args:
        pseudo_bnf (str): loaded contents of the file defining Lark grammar\
        for Pseudo-BNF.
        spl_terms (dict): dictionary containing initialized SPLTerm objects

    Raises:
        InitError: if an error with the Lark grammar occurs

    Returns:
        dict: dictionary containing lark.Tree objects, representing syntax of\
        the SPL terms
    """
    try:
        parser = LarkParser(pseudo_bnf)
    except GrammarError:
        raise InitError()

    trees = dict()
    for name, term in spl_terms.items():
        try:
            tree = parser.parse(term.get_bnf_syntax())
            trees[name] = tree
        except (UnexpectedCharacters, UnexpectedEOF):
            log_message("DEBUG", f"<{name}> could not be parsed correctly")
    return trees


def find_related_trees(name, trees):
    """Find all related syntax trees to that specified by name.

    Recursively search all available trees to resolve the most accurate
    representation of a SPL term specified by name.

    Args:
        name (str): name of a SPL term to process
        trees (dict): available syntax trees to search

    Returns:
        dict: all found related trees
    """
    visited = set()
    try:
        tree = trees[name]
        name = get_token_data(next(tree.find_data("rule_definition")))
        visited.add(name)
        tree_queue = [tree]
        while tree_queue:
            tree = tree_queue.pop(0)
            rule_names = tree.find_data("rule_name")
            for rule_name in list(rule_names):
                name = rule_name.children[0]
                if name.type == "RULE_NAME":
                    name = str(name)
                if name not in visited:
                    visited.add(name)
                    try:
                        tree_queue.append(trees[name])
                    except KeyError:
                        pass
    except KeyError:
        pass
    return choose_trees(visited, trees)


def parse_syntax_tree(tree):
    """Parse a single syntax tree.

    Looks for possible arguments, operators and functions contained in the
    tree representation of an SPL command.

    Args:
        tree (lark.Tree): syntax tree representing SPL command

    Returns:
        tuple: tuple of found arguments, functions and opreators
    """
    arguments = set()
    operators = set()
    functions = set()

    args = tree.find_data("argument")
    for a in list(args):
        arguments.add(get_token_data(a))

    ops = tree.find_data("operator_word")
    for o in list(ops):
        value = get_token_data(o)
        # if value.isupper():
        #     operators.add(value)
        operators.add(value.upper())
        if value.islower():
            functions.add(value)

    return (arguments, functions, operators)
