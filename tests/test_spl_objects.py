from spl_parser.spl_objects import SPLTerm, SPLCommand
from spl_parser.syntax_parser import build_syntax_trees

from helpers import make_path, build_terms


def test_spl_term():
    term = SPLTerm("term", "syntax")
    term.description = "description"
    assert term.get_bnf_syntax() == "<term> ::= syntax"


def test_spl_command_basic():
    command = SPLCommand("command", "syntax")
    assert command.get_bnf_syntax() == "<command> ::= syntax"


def test_spl_command_parsing(build_terms):
    with open(make_path("pseudo_bnf.lark")) as f:
        pseudo_bnf = f.read()
        trees = build_syntax_trees(pseudo_bnf, build_terms)

        command = SPLCommand("eval-command", 'eval <eval-field>=<eval-expression> ("," <eval-field>=<eval-expression>)*')
        command.parse(trees)
        assert not command.arguments
        assert len(command.functions) == 2
        assert command.functions == {"abs", "case"}

        command = SPLCommand("autoregress-command", 'autoregress <field> (AS <field:newfield>)? (p=<int:p_start>("-"<int:p_end>)?)?')
        command.parse(trees)
        assert command.arguments == {"p"}
        assert not command.functions
        assert command.operators == {"AS"}


def test_spl_command_parsing_empty():
    command = SPLCommand("eval-command", 'eval <eval-field>=<eval-expression> ("," <eval-field>=<eval-expression>)*')
    command.parse(dict())
    assert not command.arguments
    assert not command.functions
    assert not command.operators
    assert command.syntax == 'eval <eval-field>=<eval-expression> ("," <eval-field>=<eval-expression>)*'
