"""
.. module:: cli

Module cli defines functionality for the CLI part of spl_parser. The CLI
interface defines two operating modes (generate/view). Both operating modes
can be used with a remote Splunk server or with local files.
"""

import click
import os
import re
import sys

from spl_parser.spl_resource import LocalSplResource, RemoteSplResource
from spl_parser.cli_print import log_message, enable_debug
from spl_parser.exceptions import SplParserError


def validate_file(ctx, params, file):
    """Callback to validate provided local file.

    Args:
        ctx: context object obtained from click
        params: parameter object obtained from click
        file (str): name of the local file to validate

    Raises:
        click.BadParameter: if the provided file is of json, neither conf format

    Returns:
        str: the provided filename, if valid
    """
    if not file.endswith(".json") and not file.endswith(".conf"):
        raise click.BadParameter(f'"{file}" does not seem to be a valid searchbnf file.')
    return file


def validate_url(ctx, paarams, url):
    """Callback to validate provided URL.

    Performs validation of the URL towards a regular expresssion.

    Args:
        ctx: context object obtained from click
        params: parameter object obtained from click
        url (str): URL to validate

    Raises:
        click.BadParameter: if the provided URL has wrong format

    Returns:
        str: the provided URL, if valid
    """
    regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if not re.match(regex, url):
        raise click.BadParameter(f'"{url}" does not seem to be a valid URL.')
    return url


@click.group()
@click.option("--debug", is_flag=True, help="Enable debug output.")
def cli(debug, obj=None):
    """Tool for processing Splunk's Search Processing Language (SPL)."""

    if debug:
        enable_debug()


@cli.group(help="Specify local searchbnf file (.json or .conf) as SOURCE_FILE.")
@click.argument("file", metavar="SOURCE_FILE", required=True,
                type=click.Path(exists=True, readable=True), callback=validate_file)
@click.pass_context
def local(ctx, file):
    ctx.obj = LocalSplResource(file)
    log_message("INFO", f"Using local searchbnf file: {file}")


@cli.group(help="Specify URL of a remote Splunk server.")
@click.argument("url", required=True, type=str, callback=validate_url)
@click.option("--username", prompt="Splunk Username", envvar="SPLUNK_USERNAME")
@click.option("--password", prompt=True, hide_input=True, envvar="SPLUNK_PASSWORD")
@click.pass_context
def remote(ctx, url, username, password):
    ctx.obj = RemoteSplResource(url, username, password)
    log_message("INFO", f"Using remote Splunk server: {url}")


@click.command(help="View details about an SPL command.")
@click.argument("spl_command", type=str, required=True)
@click.pass_context
def view(ctx, spl_command):
    try:
        ctx.obj.view_command(spl_command)
    except SplParserError as e:
        log_message("ERROR", e)
        sys.exit(1)


@click.command(help="Generate a tmLanguage grammar for SPL.")
@click.option("-o", "--outfile", metavar="OUTPUT_FILE",
              type=click.Path(file_okay=True, writable=True),
              default="spl.tmLanguage.json",
              help="File to which the tmLanguage grammar will be saved.")
@click.pass_context
def generate(ctx, outfile):
    try:
        ctx.obj.generate_grammar(outfile)
        log_message("INFO", "SPL grammar was generated successfully!")
    except SplParserError as e:
        log_message("ERROR", e)
        log_message("ERROR", "SPL grammar was not generated!")
        sys.exit(2)


local.add_command(view)
local.add_command(generate)
remote.add_command(view)
remote.add_command(generate)
