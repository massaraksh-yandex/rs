#!/usr/bin/env python3.4 -u
import sys
from os.path import dirname, realpath
from platform.command import Command
from platform.utils import importCommands


class Rs(Command):
    def __init__(self, parent):
        super().__init__(parent)

    def name(self):
        return 'rs'

    def _commands(self):
        realPath = dirname(realpath(__file__))
        return importCommands(realPath)


if __name__ == "__main__":
    Rs(None).execute(sys.argv[1:])
    # utils.setupCodecs()
