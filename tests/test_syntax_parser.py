import pytest

from helpers import make_path, build_terms

from spl_parser.syntax_parser import choose_trees, get_token_data, build_syntax_trees, find_related_trees, parse_syntax_tree
from spl_parser.spl_objects import SPLTerm
from spl_parser.exceptions import InitError


def test_build_syntax_trees(build_terms):
    with open(make_path("pseudo_bnf.lark")) as f:
        pseudo_bnf = f.read()
        trees = build_syntax_trees(pseudo_bnf, build_terms)
        assert len(trees) == 8
        assert next(trees["fieldsummary-command"].find_data("argument")).children == ["maxvals"]
        assert get_token_data(next(trees["fieldsummary-command"].find_data("argument"))) == "maxvals"


def test_build_syntax_trees_errors():
    valid_term = SPLTerm("fieldsummary-command", "fieldsummary (maxvals=<num>)? <wc-field-list>?")
    terms = {"fieldsummary-command": valid_term}
    with pytest.raises(InitError):
        trees = build_syntax_trees("", terms)

    with open(make_path("pseudo_bnf.lark")) as f:
        pseudo_bnf = f.read()
        invalid_term = SPLTerm("term", ")(")
        terms = {"term": invalid_term}
        trees = build_syntax_trees(pseudo_bnf, terms)
        assert not trees


def test_choose_trees(build_terms):
    with open(make_path("pseudo_bnf.lark")) as f:
        pseudo_bnf = f.read()
        trees = build_syntax_trees(pseudo_bnf, build_terms)
        chosen = choose_trees(["geom-command", "file-command", "something"], trees)
        assert len(trees) == 8
        assert len(chosen) == 2
        assert "geom-command" in chosen
        assert "file-command" in chosen
        assert not "something" in chosen


def test_parse_syntax_tree(build_terms):
    with open(make_path("pseudo_bnf.lark")) as f:
        pseudo_bnf = f.read()
        trees = build_syntax_trees(pseudo_bnf, build_terms)

        a, f, o = parse_syntax_tree(trees["autoregress-command"])
        assert "AS" in o
        assert "p" in a

        a, f, o = parse_syntax_tree(trees["eval-function"])
        assert "abs" in f
        assert not a

        a, f, o = parse_syntax_tree(trees["geom-command"])
        assert "gen" in a
        assert not f
        assert not o


def test_find_related_trees(build_terms):
    with open(make_path("pseudo_bnf.lark")) as f:
        pseudo_bnf = f.read()
        trees = build_syntax_trees(pseudo_bnf, build_terms)

        found = find_related_trees("eval-command", trees)
        assert len(found) == 4
        assert {"eval-command", "eval-function", "eval-function-call", "eval-expression"} == set(found.keys())
