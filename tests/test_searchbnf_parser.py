import configparser
import json
import pytest

from helpers import make_path

from spl_parser.searchbnf_parser import parse_conf, parse_json, parse_spl_term


def test_parse_json():
    with open(make_path("searchbnf_subset.json")) as f:
        json_data = json.loads(f.read())
        terms = parse_json(json_data)
        assert len(terms) == 3
        assert "eval" in terms


def test_parse_json_error():
     with open(make_path("searchbnf_empty.json")) as f:
        with pytest.raises(json.decoder.JSONDecodeError):
            json_data = json.loads(f.read())


def test_parse_conf():
    terms = parse_conf(make_path("searchbnf_subset.conf"))
    assert len(terms) == 3
    assert "eval" in terms


def test_parse_conf_error():
    with pytest.raises(configparser.Error):
        terms = parse_conf(make_path("searchbnf_error.conf"))


def test_parse_spl_term():
    confparser = configparser.RawConfigParser(strict=False)
    confparser.read(make_path("searchbnf_subset.conf"))
    spl_term = parse_spl_term("eval-command", confparser["eval-command"])
    assert spl_term.name == "eval"
    assert spl_term.syntax == 'eval <eval-field>=<eval-expression> ("," <eval-field>=<eval-expression>)*'
