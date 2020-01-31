"""
.. module:: searchbnf_parser

This module defines functions that allow to parse searchbnf definitions in
various fomats (JSON/conf) into their Python representations for further
operations.
"""

import configparser
import json

from spl_parser.cli_print import log_message
from spl_parser.spl_objects import SPLTerm
from spl_parser.spl_objects import SPLCommand


def parse_json(json_data, parts=list()):
    """Parse searchbnf data in json format.

    The provided searchbnf data in json is processed and parsed to return all
    contained SPL terms. Optionally, only a subset of the file may be processed,
    by specifying a list containing names of the terms to be processed.

    Args:
        json_data (dict): json data containing searchbnf definitions
        parts (list, optional): names of parts to be processed. Defaults to\
        empty list(), meaning all the data.

    Returns:
        dict: dictionary of SPLTerms objects
    """
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
    """Parse searchbnf.conf file.

    The provided searchbnf.conf file is processed and parsed to return all
    contained SPL terms. Optionally, only a subset of the file may be processed,
    by specifying a list containing names of the sections to be processed.

    Args:
        conf_file (str): path to the searchbnf.conf file
        parts (list, optional): names of parts to be processed. Defaults to\
        empty list(), meaning the whole file.

    Returns:
        dict: dictionary of SPLTerms objects
    """
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
    """Parse an SPL term from the pre-loaded data.

    The provided data must have a dict-like format, representing a single
    SPL term in a standard fomat found in searchbnf.conf or searchbnf.json files.
    If the provided term is a command, an SPLCommand object is created instead
    of SPLTerm.

    Args:
        name (str): name of the term to parse
        data (dict): dict-like data representing a single SPL term

    Returns:
        SPLTerm: an initialized SPLTerm object
    """
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
