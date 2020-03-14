from platform.params.exception import PlatformException
from platform.params.params import Params
from platform.statement.rule import Rule


class Statement:
    def __init__(self, messages, result, rule):
        self.messages = messages
        self.result = result
        self.rule = rule

    def attempt(self, p: Params):
        try:
            self.rule(p)
        except PlatformException as e:
            return None
        except IndexError:
            return None

        return self.result


class InfoStatement:
    def __init__(self, messages):
        self.messages = messages

    def attempt(self, p: Params):
        return None


def emptyCommand(messages, result):
    return [ Statement(messages, result,
                       rule=lambda p: Rule(p).empty().delimers()
                                             .empty().options()
                                             .empty().targets() ) ]


def singleOptionCommand(messages, result):
    return [ Statement(messages, result,
                       lambda p: Rule(p).empty().delimers()
                                        .empty().options()
                                        .size().equals(p.targets, 1)) ]
