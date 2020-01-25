
from spl_parser.spl_term import SPLTerm


def parse_json_term(json_term):
    name = json_term["name"]
    syntax = json_term["content"]["syntax"]
    return SPLTerm(name, syntax)


def parse_json(json_dict):
    spl_terms = dict()
    json_terms = json_dict["entry"]
    for json_term in json_terms:
        spl_term = parse_json_term(json_term)
        spl_terms[spl_term.name] = spl_term.get_syntax()
    return spl_terms
