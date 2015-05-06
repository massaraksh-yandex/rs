#!/usr/bin/env python3 -u
import sys
from os.path import dirname, realpath
from platform.exception import WrongTargets
from platform.command import Command
from platform import utils


class Rs(Command):
    commands = None

    def __init__(self):
        realPath = dirname(realpath(__file__))
        self.commands = utils.importCommands(realPath)

    def help(self):
        print('rs написать что-нибудь')

    def check(self, p):
        if p.targets[0] not in self.commands:
            raise WrongTargets('Нет такой команды: {0}'.format(p.targets[0]))

    def process(self, p):
        cmd = p.argv[0]
        self.commands[cmd]().execute(p.argv[1:])


if __name__ == "__main__":
    utils.setupCodecs()
    Rs().execute(sys.argv[1:])