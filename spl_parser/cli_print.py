"""
.. module:: cli_print

This module defines functions for easy and pretty printing of messages to
terminal. This is ensured using click package.
"""

import click

DEBUG_ENABLED = False

levels = {
            "ERROR": click.style("ERROR", fg="red", bold=True),
            "WARNING": click.style("WARNING", fg="magenta", bold=True),
            "INFO": click.style("INFO", fg="green", bold=True),
            "DEBUG": click.style("DEBUG", fg="white", bold=True)
        }


def log_message(level, message):
    """Print log message to the terminal by using click.

    Debugging must be enabled to print DEBUG messages.

    Args:
        level (str): The level of the message. One of ERROR, WARNING, INFO,\
             or DEBUG
        message (str): The message to print.
    """
    if level == "DEBUG" and not DEBUG_ENABLED:
        return
    click.echo(f"{levels[level]}: {message}", err=(level == "ERROR"))


def enable_debug():
    """Enable debugging."""
    global DEBUG_ENABLED
    DEBUG_ENABLED = True


def print_kv(key, value):
    """Print key-value pair to the terminal.

    Key is printed in bold style, whereas the value is printed normally.

    Args:
        key (str)
        value (str)
    """
    key = click.style(key, bold=True)
    click.echo(f"{key}: {value}")
