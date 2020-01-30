import configparser
import json

from spl_parser.cli_print import log_message
from spl_parser.spl_objects import SPLTerm
from spl_parser.spl_objects import SPLCommand


def parse_json(json_data, parts=list()):
    spl_terms = dict()

    if parts:
        json_terms = [x for x in json_data["entry"] if x["name"] in parts]
    else:
        json_terms = json_data["entry"]

    for json_term in json_terms:
        try:
            spl_term = parse_spl_term(json_term["name"], json_term["content"])
            spl_terms[spl_term.name] = spl_term
        except KeyError:
            log_message("WARNING", f"{json_term['name']} has incorrect format.")

    return spl_terms


def parse_conf(conf_file, parts=list()):
    confparser = configparser.RawConfigParser(strict=False)
    confparser.read(conf_file)
    spl_terms = dict()

    if parts:
        for part in parts:
            try:
                spl_term = parse_spl_term(part, confparser[part])
                spl_terms[spl_term.name] = spl_term
            except KeyError:
                pass
    else:
        for section in confparser.sections():
            try:
                spl_term = parse_spl_term(section, confparser[section])
                spl_terms[spl_term.name] = spl_term
            except KeyError:
                log_message("WARNING", f"{section} has incorrect format.")

    return spl_terms


def parse_spl_term(name, data):
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
