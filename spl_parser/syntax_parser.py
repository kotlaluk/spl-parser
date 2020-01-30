from lark import Lark
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF

from spl_parser.cli_print import log_message


class LarkParser:
    def __init__(self, grammar):
        self.__parser =  Lark(grammar, parser="earley")

    def parse(self, expression):
        return self.__parser.parse(expression)


def choose_trees(names, trees):
    chosen = dict()
    for name in names:
        try:
            chosen[name] = trees[name]
        except KeyError:
            pass
    return chosen


def get_token_data(subtree):
    return str(subtree.children[0])


def build_syntax_trees(pseudo_bnf, spl_terms):
    parser = LarkParser(pseudo_bnf)
    trees = dict()
    for name, term in spl_terms.items():
        try:
            tree = parser.parse(term.get_bnf_syntax())
            trees[name] = tree
        except (UnexpectedCharacters, UnexpectedEOF):
            log_message("DEBUG", f"<{name}> could not be parsed correctly")
    return trees


def find_related_trees(name, trees):
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
    arguments = set()
    operators = set()
    functions = set()

    args = tree.find_data("argument")
    for a in list(args):
        arguments.add(get_token_data(a))

    ops = tree.find_data("operator_word")
    for o in list(ops):
        value = get_token_data(o)
        if value.isupper():
            operators.add(value)
        if value.islower():
            functions.add(value)

    return (arguments, functions, operators)
