from spl_parser.lark_parser import LarkParser


def choose_commands(trees):
    commands = dict()
    for name in trees.keys():
        if name.endswith("-command"):
            commands[name] = trees[name]
    return commands


def build_syntax_trees(spl_terms):
    with open("pseudo_bnf.lark") as f:
        parser = LarkParser(f.read())
    trees = dict()
    for name, term in spl_terms.items():
        tree = parser.parse(term.get_syntax())
        trees[name] = tree
    return trees


def member_trees(name, trees):
    tree = trees[name]
    visited = set()
    name = str(next(tree.find_data("rule_definition")).children[0])
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
                tree_queue.append(trees[name])
    return visited
