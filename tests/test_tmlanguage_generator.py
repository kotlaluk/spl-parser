import json
import os

from helpers import make_path

from spl_parser.tmlanguage_generator import TmLanguageGenerator
from spl_parser.spl_objects import SPLCommand


def test_init():
    with open(make_path("template.tmLanguage.json")) as f:
        gen = TmLanguageGenerator(f.read())
        assert "include" in gen.commands_entry
        assert gen.commands_entry["include"] == "#commands.<example_command>"

        assert "<example_command_alias>" in gen.commands_block["begin"]
        assert "<example_operator>" in gen.operators_block["match"]
        assert "support.function.spl" in gen.functions_block["captures"]["1"]["name"]
        assert "<example_argument>" in gen.arguments_block["patterns"][0]["match"]


def test_generate_include():
    with open(make_path("template.tmLanguage.json")) as f:
        gen = TmLanguageGenerator(f.read())
        assert gen.generate_include("stats", "command") == {"include": "#command.stats"}


def test_add_command():
    with open(make_path("template.tmLanguage.json")) as f:
        gen = TmLanguageGenerator(f.read())
        command = SPLCommand("autoregress", "syntax")
        command.arguments = {"arg1"}
        command.operators = {"AS"}

        gen.add_command(command)
        assert "commands.autoregress" in gen.grammar["repository"]
        assert "arguments.autoregress" in gen.grammar["repository"]
        assert "arg1" in gen.grammar["repository"]["arguments.autoregress"]["patterns"][0]["match"]
        assert "operators.autoregress" in gen.grammar["repository"]
        assert "functions.autoregress" not in gen.grammar["repository"]


def test_save_grammar():
    with open(make_path("template.tmLanguage.json")) as f:
        gen = TmLanguageGenerator(f.read())
        command = SPLCommand("command", "syntax")
        gen.add_command(command)
        gen.save_grammar(make_path("test_output.json"))

    with open(make_path("test_output.json")) as f:
        content = json.loads(f.read())
        assert content == gen.grammar
    os.remove(make_path("test_output.json"))
