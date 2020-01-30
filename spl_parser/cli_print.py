import click

DEBUG_ENABLED = False

levels = {
            "ERROR": click.style("ERROR", fg="red", bold=True),
            "WARNING": click.style("WARNING", fg="magenta", bold=True),
            "INFO": click.style("INFO", fg="green", bold=True),
            "DEBUG": click.style("DEBUG", fg="white", bold=True)
        }


def log_message(level, message):
    if level == "DEBUG" and not DEBUG_ENABLED:
        return
    click.echo(f"{levels[level]}: {message}", err=(level == "ERROR"))


def enable_debug():
    global DEBUG_ENABLED
    DEBUG_ENABLED = True


def print_kv(key, value):
    key = click.style(key, bold=True)
    click.echo(f"{key}: {value}")
