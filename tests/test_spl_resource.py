import pytest

from helpers import make_path

from spl_parser.spl_resource import SplResource, LocalSplResource, RemoteSplResource
from spl_parser.exceptions import ParsingError


def test_base_spl_resource():
    spl_resource = SplResource()
    assert type(spl_resource.spl_terms) is dict
    with pytest.raises(NotImplementedError):
        spl_resource.view_command("command")
    with pytest.raises(NotImplementedError):
        spl_resource.generate_grammar("outfile")


@pytest.mark.parametrize("file", ["searchbnf_empty.json", "searchbnf_error.conf", "searchbnf_error.json"])
def test_local_fetch_spl_terms_errors(file):
    spl_resource = LocalSplResource(make_path(file))
    with pytest.raises(ParsingError):
        spl_resource.fetch_spl_terms()


@pytest.mark.parametrize("file", ["searchbnf_subset.json", "searchbnf_subset.conf"])
def test_local_fetch_spl_terms(file):
    resource = LocalSplResource(make_path(file))
    resource.fetch_spl_terms()
    assert len(resource.spl_terms) == 3

    resource.fetch_spl_terms(["stats-command", "abstract-command"])
    assert len(resource.spl_terms) == 2

    stats = resource.spl_terms["stats"]
    assert stats.name == "stats"
    assert stats.syntax == "stats <stats-command-arguments>"
    assert stats.description
