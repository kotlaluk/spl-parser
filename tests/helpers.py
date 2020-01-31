import pytest
from pathlib import Path

from spl_parser.spl_objects import SPLTerm, SPLCommand


def make_path(name):
    return f"{str(Path(__file__).parent)}/fixtures/{name}"


@pytest.fixture
def build_terms():
    terms = dict()
    terms.update({"fieldsummary-command": SPLCommand("fieldsummary-command", "fieldsummary (maxvals=<num>)? <wc-field-list>?")})
    terms.update({"file-command": SPLCommand("fieldsummary-command", "file <filename>")})
    terms.update({"geom-command": SPLCommand("geom-command", "geom (<featureCollection>)? (<allFeatures>)? (<featureIdField>)? (gen=<num>)?")})
    terms.update({"eval-function": SPLTerm("eval-function", "abs|case")})
    terms.update({"eval-command": SPLCommand("eval-command", 'eval <eval-field>=<eval-expression> ("," <eval-field>=<eval-expression>)*')})
    terms.update({"eval-expression": SPLTerm("eval-expression", "<eval-math-exp> | <eval-concat-exp> | <eval-compare-exp> | <eval-bool-exp> | <eval-function-call>")})
    terms.update({"eval-function-call": SPLTerm("eval-function-call", '<eval-function> "(" <eval-expression> ("," <eval-expression>)* ")"')})
    terms.update({"autoregress-command": SPLCommand("autoregress-command", 'autoregress <field> (AS <field:newfield>)? (p=<int:p_start>("-"<int:p_end>)?)?')})
    return terms
