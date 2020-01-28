from spl_parser.spl_objects import SPLTerm
from spl_parser.spl_objects import SPLCommand


def parse_json_term(json_term):
    # TODO global try/except - logging
    name = json_term["name"]
    syntax = json_term["content"]["syntax"]
    if name.endswith("-command"):
        name = name.replace("-command", "")

        # Get aliases if present
        try:
            aliases = json_term["content"]["alias"].split(",")
        except KeyError:
            aliases = list()

        spl_term = SPLCommand(name, syntax)
        spl_term.aliases = aliases
    else:
        spl_term = SPLTerm(name, syntax)

    # Optionally fetch description
    try:
        description = json_term["content"]["description"]
        spl_term.description = description
    except KeyError:
        pass
    return spl_term


def parse_json(json_data):
    spl_terms = dict()
    json_terms = json_data["entry"]
    for json_term in json_terms:
        spl_term = parse_json_term(json_term)
        spl_terms[spl_term.name] = spl_term
    return spl_terms
