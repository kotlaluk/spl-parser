import click
import re
import sys

from spl_parser.spl_resource import LocalSplResource, RemoteSplResource
from spl_parser.cli_print import log_message
from spl_parser.exceptions import SplParserError


def validate_file(ctx, params, file):
    if not file.endswith(".json") and not file.endswith(".conf"):
        raise click.BadParameter(f'"{file}" does not seem to be a valid searchbnf file.')
    return file


def validate_url(ctx, paarams, url):
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
def cli(obj=None):
    """Tool for processing Splunk's Search Processing Language (SPL)."""
    pass


@cli.group(help="Specify a local searchbnf file (.json or .conf) as SOURCE_FILE.")
@click.argument("file", metavar="SOURCE_FILE", required=True,
                type=click.Path(exists=True, readable=True), callback=validate_file)
@click.pass_context
def local(ctx, file):
    ctx.obj = LocalSplResource(file)
    log_message("INFO", f"Using local searchbnf file: {file}")


@cli.group(help="Specify URL of a remote Splunk server.")
@click.argument("url", required=True, type=str, callback=validate_url)
@click.pass_context
def remote(ctx, url):
    ctx.obj = RemoteSplResource(url)
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
@click.option("-o", "--outfile", metavar="OUTPUT_FILE", type=click.Path(file_okay=True, writable=True),
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
