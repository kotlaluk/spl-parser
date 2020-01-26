from spl_parser.lark_parser import LarkParser
from spl_parser.spl_term import SPLCommand


def choose_commands(trees):
    commands = dict()
    for name in trees.keys():
        if name.endswith("-command"):
            commands[name] = trees[name]
    return commands


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


def build_syntax_trees(spl_terms):
    with open("spl_parser/grammars/pseudo_bnf.lark") as f:
        parser = LarkParser(f.read())
    trees = dict()
    for name, term in spl_terms.items():
        tree = parser.parse(term.get_syntax())
        trees[name] = tree
    return trees


def member_trees(name, trees):
    tree = trees[name]
    visited = set()
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
    return visited


def parse_command(name, member_trees):
    command = SPLCommand(name)
    for tree in member_trees.values():
        (arguments, functions, operators) = parse_tree(tree)
        command.add_arguments(arguments)
        command.add_operators(operators)
        command.add_functions(functions)
    return command


def parse_tree(tree):
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
