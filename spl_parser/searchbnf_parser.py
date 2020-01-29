import configparser
import json

from spl_parser.spl_objects import SPLTerm
from spl_parser.spl_objects import SPLCommand


def parse_json(json_file):
    with open(json_file) as f:
        json_data = json.loads(f.read())
        spl_terms = dict()
        for json_term in json_data["entry"]:
            spl_term = parse_spl_term(json_term["name"], json_term["content"])
            spl_terms[spl_term.name] = spl_term
        return spl_terms


def parse_conf(conf_file):
    confparser = configparser.RawConfigParser(strict=False, allow_no_value=True)
    confparser.read(conf_file)
    spl_terms = dict()
    for section in confparser.sections():
        spl_term = parse_spl_term(section, confparser[section])
        spl_terms[spl_term.name] = spl_term
    return spl_terms


def parse_spl_term(name, data):
    # TODO global try/except - logging
    syntax = data["syntax"]
    if name.endswith("-command"):
        name = name.replace("-command", "")

        # Get aliases if present
        try:
            aliases = [x.strip() for x in data["alias"].split(",")]
        except KeyError:
            aliases = list()

        spl_term = SPLCommand(name, syntax)
        spl_term.aliases = aliases
    else:
        spl_term = SPLTerm(name, syntax)

    # Optionally fetch description
    try:
        description = data["description"]
        spl_term.description = description
    except KeyError:
        pass
    return spl_term
