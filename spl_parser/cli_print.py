import click


def log_message(level, message):
    levels = {
        "ERROR": click.style("ERROR", fg="red", bold=True),
        "WARNING": click.style("WARNING", fg="magenta", bold=True),
        "INFO": click.style("INFO", fg="green", bold=True),
        "DEBUG": click.style("DEBUG", fg="white", bold=True)
    }
    click.echo(f"{levels[level]}: {message}", err=(level == "ERROR"))


def print_kv(key, value):
    key = click.style(key, bold=True)
    click.echo(f"{key}: {value}")
