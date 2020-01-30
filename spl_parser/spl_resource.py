import aiohttp
import asyncio
import importlib.resources as pkg_resources
import json

from spl_parser.searchbnf_parser import parse_conf, parse_json
from spl_parser.spl_objects import SPLCommand
from spl_parser.syntax_parser import build_syntax_trees
from spl_parser.tmlanguage_generator import TmLanguageGenerator
from spl_parser.cli_print import log_message
from spl_parser.exceptions import CommandNotFoundError, ParsingError,\
                                  AuthenticationError, ConnectionError


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

        pseudo_bnf = pkg_resources.read_text("spl_parser.grammars",
                                             "pseudo_bnf.lark")
        tm_template = pkg_resources.read_text("spl_parser.templates",
                                              "template.tmLanguage.json")
        generator = TmLanguageGenerator(tm_template)

        log_message("INFO", "Building syntax trees...")
        trees = build_syntax_trees(pseudo_bnf, self.spl_terms)

        log_message("INFO", "Parsing SPL commands...")
        commands = [x for x in self.spl_terms.values()\
                    if isinstance(x, SPLCommand)]
        for command in commands:
            command.parse(trees)
            generator.add_command(command)

        log_message("INFO", f"Saving grammar to file {outfile}...")
        generator.save_grammar(outfile)


class LocalSplResource(SplResource):
    def __init__(self, file):
        super().__init__()
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
    def __init__(self, url, username, password):
        super().__init__()
        self.url = url
        if self.url[-1] == "/":
            self.url = self.url[:-1]
        self.headers = dict()
        self.headers["Accept"] = "application/json"
        self.auth = aiohttp.BasicAuth(username, password)

    def build_url(self, term_name=None):
        url = f"{self.url}/servicesNS/-/-/configs/conf-searchbnf"
        if term_name:
            return f"{url}/{term_name}/?count=0&output_mode=json"
        return f"{url}?count=0&output_mode=json"

    def fetch_spl_terms(self, spl_terms=list()):
        asyncio.run(self.async_fetch_spl_terms(spl_terms))


    async def async_fetch_spl_terms(self, spl_terms):
        self.session = aiohttp.ClientSession(headers=self.headers,
                        connector=aiohttp.TCPConnector(verify_ssl=False),
                        auth=self.auth, raise_for_status=True)

        async with self.session:
            try:
                if not spl_terms:
                    json_data = await self.async_get(self.build_url())
                    for term in json_data["entry"]:
                        try:
                            spl_terms.append(term["name"])
                        except KeyError:
                            pass

                await asyncio.gather(*[self.async_fetch_spl_term(term)\
                                       for term in spl_terms])

            except aiohttp.client_exceptions.ClientResponseError as e:
                if e.code == 401:
                    raise AuthenticationError()
                else:
                    log_message("DEBUG", str(e))
                    raise ConnectionError()
            except aiohttp.client_exceptions.ClientConnectorError as e:
                log_message("DEBUG", str(e))
                raise ConnectionError()

    async def async_fetch_spl_term(self, spl_term):
        url = self.build_url(spl_term)
        try:
            json_data = await self.async_get(url)
            log_message("DEBUG", f"<{spl_term}> was fetched")
            spl_terms = parse_json(json_data, [spl_term])
            self.spl_terms.update(spl_terms)
        except aiohttp.client_exceptions.ClientResponseError as e:
            if e.code == 404:
                log_message("DEBUG", f"<{spl_term}> was NOT fetched")
            else:
                raise e

    async def async_get(self, url):
        async with self.session.get(url) as response:
            return await response.json()
