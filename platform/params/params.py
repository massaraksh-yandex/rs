from collections import namedtuple
from platform.params.delimer import DoubleDelimer, SingleDelimer
from platform.params.exception import WrongDelimers
from platform.utils.keydefaultdict import keydefaultdict


def isOption(arg):
    return arg.startswith('--') and arg != '--'


def isDelimer(arg):
    return arg == SingleDelimer.value or arg == DoubleDelimer.value


def createdelimer(delimer, index):
    if delimer == SingleDelimer.value:
        return SingleDelimer(index)
    elif delimer == DoubleDelimer.value:
        return DoubleDelimer(index)
    else:
        raise WrongDelimers('Не могу создать разделитель: {0}, {1}'.format(delimer, index))


def _parseOption(arg):
    opt = arg[2:].split('=', 1)
    return (opt[0], None if len(opt) == 1 else opt[1])


Target = namedtuple('Target', ['value', 'index'])


class Params:
    def __init__(self, args):
        self.argv = args
        self.options = keydefaultdict(lambda x: None)
        self.targets = []
        self.delimers = []

        index = 0
        for arg in self.argv:
            if isOption(arg):
                k, v = _parseOption(arg)
                self.options[k] = v
            elif isDelimer(arg):
                self.delimers.append(createdelimer(arg, index))
            else:
                self.targets.append(Target(value=arg, index=index))
                index += 1

        self.needHelp = 'help' in self.options

        self.delimered = []
        last = 0
        for d in self.delimers:
            self.delimered.append(self.targets[last:d.index])
            last = d.index
        self.delimered.append(self.targets[last:])
