from lark import Lark


class LarkParser:
    def __init__(self, grammar):
        self.__parser =  Lark(grammar, parser="lalr")

    def parse(self, expression):
        return self.__parser.parse(expression)
