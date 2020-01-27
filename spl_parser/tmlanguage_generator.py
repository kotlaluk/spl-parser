from copy import deepcopy
import json


COMMAND_PLACEHOLDER = "<example_command>"
ALIAS_PLACEHOLDER = "<example_alias>"
ARGUMENT_PLACEHOLDER = "<example_argument>"
FUNCTION_PLACEHOLDER = "<example_function>"
OPERATOR_PLACEHOLDER = "<example_operator>"


class TmLanguageGenerator:
    def __init__(self, path_to_template):
        with open(path_to_template) as f:
            template_data = f.read()
        # TODO try/except
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

    def generate_grammar_block(self, name, template_block, source=None, targets=list()):
        block_str = json.dumps(template_block)
        block_str = block_str.replace(COMMAND_PLACEHOLDER, name)
        if source is not None:
            if len(targets) == 0:
                block_str = block_str.replace(source, "")
            else:
                if len(targets) > 1:
                    for target in targets[:-1]:
                        block_str = block_str.replace(source, f"{target}|{source}")
                block_str = block_str.replace(source, targets[-1])
        return json.loads(block_str)

    def add_command(self, spl_command):
        # Generate grammar blocks from the command and insert them into the grammar
        commands_entry = self.generate_grammar_block(spl_command.name, self.commands_entry)
        commands_block = self.generate_grammar_block(spl_command.name, self.commands_block, source=ALIAS_PLACEHOLDER, targets=spl_command.aliases)
        arguments_block = self.generate_grammar_block(spl_command.name, self.arguments_block, source=ARGUMENT_PLACEHOLDER, targets=spl_command.arguments)
        functions_block = self.generate_grammar_block(spl_command.name, self.functions_block, source=FUNCTION_PLACEHOLDER, targets=spl_command.functions)
        operators_block = self.generate_grammar_block(spl_command.name, self.operators_block, source=OPERATOR_PLACEHOLDER, targets=spl_command.operators)

        self.grammar["repository"]["commands"]["patterns"].append(commands_entry)
        self.grammar["repository"][f"commands.{spl_command.name}"] = commands_block
        self.grammar["repository"][f"arguments.{spl_command.name}"] = arguments_block
        self.grammar["repository"][f"functions.{spl_command.name}"] = functions_block
        self.grammar["repository"][f"operators.{spl_command.name}"] = operators_block

    def save_grammar(self, outfile):
        # TODO make backup if file exists
        with open(outfile, "w") as f:
            f.write(json.dumps(self.grammar, indent=4))
