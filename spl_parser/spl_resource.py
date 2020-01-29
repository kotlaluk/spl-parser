import importlib.resources as pkg_resources

from spl_parser.searchbnf_parser import parse_conf, parse_json
from spl_parser.spl_objects import SPLCommand
from spl_parser.syntax_parser import build_syntax_trees
from spl_parser.tmlanguage_generator import TmLanguageGenerator


class SplResource:
    def __init__(self):
        self.spl_terms = dict()

    def fetch_spl_terms(self, spl_terms=list()):
        raise NotImplementedError()

    def view_command(self, command):
        self.fetch_spl_terms([f"{command}-command"])

        if self.spl_terms:
            for spl_term in self.spl_terms.values():
                spl_term.print()
        else:
            # TODO
            print("error")

    def generate_grammar(self, outfile):
        self.fetch_spl_terms()

        pseudo_bnf = pkg_resources.read_text("spl_parser.grammars", "pseudo_bnf.lark")
        tm_template = pkg_resources.read_text("spl_parser.templates", "template.tmLanguage.json")

        trees = build_syntax_trees(pseudo_bnf, self.spl_terms)

        generator = TmLanguageGenerator(tm_template)

        commands = [x for x in self.spl_terms.values() if isinstance(x, SPLCommand)]

        for command in commands:
            command.find_related_trees(trees)
            command.parse()
            generator.add_command(command)

        generator.save_grammar(outfile)


class LocalSplResource(SplResource):
    def __init__(self, file):
        self.file = file

    def fetch_spl_terms(self, spl_terms=list()):
        if self.file.endswith(".conf"):
            self.spl_terms = parse_conf(self.file, spl_terms)
        if self.file.endswith(".json"):
            self.spl_terms = parse_json(self.file, spl_terms)


class RemoteSplResource(SplResource):
    def __init__(self, url):
        self.url = url

    def fetch_spl_terms(self, spl_terms=list()):
        raise NotImplementedError()
