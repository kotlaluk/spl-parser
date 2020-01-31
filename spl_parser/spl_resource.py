"""
.. module:: spl_resource

Module spl_resource contains definition of the workflow for the main
functionalities of the package - generating the grammar and viewing commands.
These functionalities are performed on objects called SplResource. Based on the
operation mode, a LocalSplResource, or a RemoteSplResource is used.
"""

import aiohttp
import asyncio
import configparser
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
    """Base class defining SplResource"""
    def __init__(self):
        self.spl_terms = dict()

    def fetch_spl_terms(self, spl_terms=list()):
        """Fetch information for SPL terms from the resource.

        Args:
            spl_terms (list, optional): names of SPL terms to be fetched.\
                Defaults to empty list(), meaning all available resources.
        """
        raise NotImplementedError()

    def view_command(self, command):
        """View details about an SPL command.

        Performs all necessary steps to fetch, process and view information
        about the provided command. The command details and informational
        messages are printed to terminal.

        Args:
            command (str): name of the command to view

        Raises:
            CommandNotFoundError: if the specified command was not found
        """
        log_message("INFO", f"Fetching details about {command} command...")
        self.fetch_spl_terms([f"{command}-command"])

        if self.spl_terms:
            log_message("INFO", f"Found results:")
            for spl_term in self.spl_terms.values():
                spl_term.print()
        else:
            raise CommandNotFoundError(command)

    def generate_grammar(self, outfile):
        """Generate a tmLanguage grammar for SPL.

        Performs all necessary steps to fetch, process, build and generate
        a tmLanguage grammar file for SPL. Informational messages are printed
        to terminal during the generation process.

        Args:
            outfile (str): name of the file to save the generated grammar into
        """
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
    """Class defining an SPL resource based on a local file."""
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
        except (KeyError, ValueError, configparser.Error):
            raise ParsingError(self.file)


class RemoteSplResource(SplResource):
    """Class defining an SPL resource based on a remote Splunk server."""
    def __init__(self, url, username, password):
        """
        Args:
            url (str): URL of a remote Splunk server
            username (str): username to authenticate to the remote Splunk server
            password (str): password corresponding to the username
        """
        super().__init__()
        self.url = url
        if self.url[-1] == "/":
            self.url = self.url[:-1]
        self.headers = dict()
        self.headers["Accept"] = "application/json"
        self.auth = aiohttp.BasicAuth(username, password)

    def build_url(self, term_name=None):
        """Build a URL for the searchbnf file on the remote Splunk server.

        If a term is specified, builds URL for the specific term, otherwise
        builds URL for all terms.

        Args:
            term_name (str, optional): name of the term. Defaults to None\
            (all terms).

        Returns:
            str: the build URL
        """
        url = f"{self.url}/servicesNS/-/-/configs/conf-searchbnf"
        if term_name:
            return f"{url}/{term_name}/?count=0&output_mode=json"
        return f"{url}?count=0&output_mode=json"

    def fetch_spl_terms(self, spl_terms=list()):
        asyncio.run(self.async_fetch_spl_terms(spl_terms))

    async def async_fetch_spl_terms(self, spl_terms):
        """Asynchronously fetch details about SPL terms.

        Args:
            spl_terms (list): SPL terms to retrieve
        """
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
        """Asynchronously fetch details about an SPL term.

        Args:
            spl_term (SPLTerm): SPL term to retrieve
        """
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
        """Perform asynchronous GET request.

        Args:
            url (str): URL to use

        Returns:
            dict: JSON data received as response
        """
        async with self.session.get(url) as response:
            return await response.json()
