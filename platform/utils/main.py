from collections import namedtuple
from os.path import join, pardir, dirname, realpath
from platform.commands.command import Command
from platform.db.config import Config
from platform.db.database import Database
from platform.db.settings import Settings
from platform.utils.utils import importCommands, setupCodecs
import sys


ConfigHooks = namedtuple('ConfigHooks', ['checkfiles', 'createfiles', 'saveconfig', 'createdatabase'])


def main(name, information, hooks = ConfigHooks(checkfiles=lambda: True,
                                                createfiles=lambda: None,
                                                saveconfig=lambda: None,
                                                createdatabase=lambda: None)):
    class MainCommand(Command):
        def __init__(self, name, database):
            super().__init__(None, database)
            self._name = name
            self._realpath = join(__file__, pardir, pardir)

        def name(self):
            return self._name

        def _info(self):
            return information

        def _commands(self):
            realPath = dirname(realpath(self._realpath))
            return importCommands(realPath)

    setupCodecs()

    if not hooks.checkfiles():
        hooks.createfiles()
        hooks.saveconfig()
    MainCommand(name, hooks.createdatabase()).execute(sys.argv[1:])
