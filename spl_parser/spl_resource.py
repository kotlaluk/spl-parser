import importlib.resources as pkg_resources
import json

from spl_parser.searchbnf_parser import parse_conf, parse_json
from spl_parser.spl_objects import SPLCommand
from spl_parser.syntax_parser import build_syntax_trees
from spl_parser.tmlanguage_generator import TmLanguageGenerator
from spl_parser.cli_print import log_message
from spl_parser.exceptions import CommandNotFoundError, ParsingError


class SplResource:
    def __init__(self):
        self.spl_terms = dict()

    def fetch_spl_terms(self, spl_terms=list()):
        raise NotImplementedError()

    def view_command(self, command):
        log_message("INFO", f"Fetching details about {command} command...")
        self.fetch_spl_terms([f"{command}-command"])

        if self.spl_terms:
            log_message("INFO", f"Found results:")
            for spl_term in self.spl_terms.values():
                spl_term.print()
        else:
            raise CommandNotFoundError(command)

    def generate_grammar(self, outfile):
        log_message("INFO", f"Fetching all SPL terms...")
        self.fetch_spl_terms()

        pseudo_bnf = pkg_resources.read_text("spl_parser.grammars", "pseudo_bnf.lark")
        tm_template = pkg_resources.read_text("spl_parser.templates", "template.tmLanguage.json")
        generator = TmLanguageGenerator(tm_template)

        log_message("INFO", "Building syntax trees...")
        trees = build_syntax_trees(pseudo_bnf, self.spl_terms)

        log_message("INFO", "Parsing SPL commands...")
        commands = [x for x in self.spl_terms.values() if isinstance(x, SPLCommand)]
        for command in commands:
            command.parse(trees)
            generator.add_command(command)

        log_message("INFO", f"Saving grammar to file {outfile}...")
        generator.save_grammar(outfile)


class LocalSplResource(SplResource):
    def __init__(self, file):
        self.file = file

    def fetch_spl_terms(self, spl_terms=list()):
        try:
            if self.file.endswith(".conf"):
                self.spl_terms = parse_conf(self.file, spl_terms)
            if self.file.endswith(".json"):
                with open(self.file) as f:
                    json_data = json.loads(f.read())
                self.spl_terms = parse_json(json_data, spl_terms)
        except KeyError:
            raise ParsingError(self.file)


class RemoteSplResource(SplResource):
    def __init__(self, url):
        self.url = url

    def fetch_spl_terms(self, spl_terms=list()):
        raise NotImplementedError()
