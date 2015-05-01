#!/usr/bin/env python3
import sys
import codecs
from os.path import dirname, realpath

from platform.exception import WrongTargets
from platform.command import Command
from src.projects_repo import Repo
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
            raise WrongTargets('Нет такой цели: {0}'.format(t))

    def process(self, p):
        cmd = p.argv[0]
        self.commands[cmd]().execute(p.argv[1:])


if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    Repo.parse()
    Rs().execute(sys.argv[1:])





