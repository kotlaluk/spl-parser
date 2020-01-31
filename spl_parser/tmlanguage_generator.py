"""
.. module:: tmlanguage_generator

Module defining functionality related to generating a TmLanguage grammar for SPL.
"""

from copy import deepcopy
import json


COMMAND_PLACEHOLDER = "<example_command>"
ALIAS_PLACEHOLDER = "<example_command_alias>"
ARGUMENT_PLACEHOLDER = "<example_argument>"
FUNCTION_PLACEHOLDER = "<example_function>"
OPERATOR_PLACEHOLDER = "<example_operator>"


class TmLanguageGenerator:
    """Class defining a TmLanguage generator."""

    def __init__(self, template_data):
        """
        Args:
            template_data (str): contents of the file defining a tmLanguage template
        """
        self.template = json.loads(template_data)
        self.__parse_template()

    def __parse_template(self):
        # Retrieve object patterns
        self.commands_entry = self.template["repository"]["commands"]["patterns"][0]
        self.commands_block = self.template["repository"][f"commands.{COMMAND_PLACEHOLDER}"]
        self.arguments_block = self.template["repository"][f"arguments.{COMMAND_PLACEHOLDER}"]
        self.functions_block = self.template["repository"][f"functions.{COMMAND_PLACEHOLDER}"]
        self.operators_block = self.template["repository"][f"operators.{COMMAND_PLACEHOLDER}"]

        # Remove example objects
        empty_template = deepcopy(self.template)
        empty_template["repository"]["commands"]["patterns"] = list()
        del empty_template["repository"][f"commands.{COMMAND_PLACEHOLDER}"]
        del empty_template["repository"][f"arguments.{COMMAND_PLACEHOLDER}"]
        del empty_template["repository"][f"functions.{COMMAND_PLACEHOLDER}"]
        del empty_template["repository"][f"operators.{COMMAND_PLACEHOLDER}"]
        self.grammar = empty_template

    def generate_include(self, name, type):
        """Generate "include" line for the grammar.

        Args:
            name (str): name of a term
            type (str): type of the include, e.g. "commands"

        Returns:
            str: the generated "include" line
        """
        return {"include": f"#{type}.{name}"}

    def generate_grammar_block(self, name, template_block, source, targets):
        """Generate whole block for the grammar.

        Generates a block that can be included in the grammar, based on the loaded
        parts from the template. Performs replacement of the placeholders defined
        in the gramars for the actual values

        Args:
            name (str): name of the command to work with
            template_block (dict): a template grammar block to be used
            source (str): a placeholder to be replaced
            targets (list): the actual values for replacement
        """
        targets = list(targets)
        block_str = json.dumps(template_block)
        if len(targets) > 1:
            for target in targets[:-1]:
                block_str = block_str.replace(source, f"{target}|{source}")
        block_str = block_str.replace(source, targets[-1])
        return json.loads(block_str)

    def add_command(self, spl_command):
        """Add SPLCommand to the grammar.

        Performs all necessary steps (generating, inserting) to include a whole
        SPL command in the resulting grammar.

        Args:
            spl_command (SPLCommand): an SPL command to include
        """

        # Generate grammar blocks from the command and insert them into the grammar
        command_aliases = [spl_command.name] + spl_command.aliases
        commands_block = self.generate_grammar_block(spl_command.name, self.commands_block,
                         source=ALIAS_PLACEHOLDER, targets=command_aliases)
        self.grammar["repository"]["commands"]["patterns"]\
            .append(self.generate_include(spl_command.name, "commands"))
        self.grammar["repository"][f"commands.{spl_command.name}"] = commands_block

        if spl_command.arguments:
            arguments_block = self.generate_grammar_block(spl_command.name, self.arguments_block,
                                source=ARGUMENT_PLACEHOLDER, targets=spl_command.arguments)
            self.grammar["repository"][f"commands.{spl_command.name}"]["patterns"]\
                .append(self.generate_include(spl_command.name, "arguments"))
            self.grammar["repository"][f"arguments.{spl_command.name}"] = arguments_block

        if spl_command.functions:
            functions_block = self.generate_grammar_block(spl_command.name, self.functions_block,
                                source=FUNCTION_PLACEHOLDER, targets=spl_command.functions)
            self.grammar["repository"][f"commands.{spl_command.name}"]["patterns"]\
                .append(self.generate_include(spl_command.name, "functions"))
            self.grammar["repository"][f"functions.{spl_command.name}"] = functions_block

        if spl_command.operators:
            operators_block = self.generate_grammar_block(spl_command.name, self.operators_block,
                                source=OPERATOR_PLACEHOLDER, targets=spl_command.operators)
            self.grammar["repository"][f"commands.{spl_command.name}"]["patterns"]\
                .append(self.generate_include(spl_command.name, "operators"))
            self.grammar["repository"][f"operators.{spl_command.name}"] = operators_block

    def save_grammar(self, outfile):
        """Save the generated grammar to the specified file.

        Args:
            outfile (str): name of the file to save the grammar into
        """
        with open(outfile, "w") as f:
            f.write(json.dumps(self.grammar, indent=4))
