from os.path import join
from os.path import isfile
import subprocess

from src.settings import Settings
from src.repo import getProjects


class SyncData:
    project = None
    path = ''
    host = ''
    exclude_from = ''

    def __init__(self, name):
        self.project = getProjects()[name]
        self.path = self.project.path
        self.host = self.project.host
        exc = join(Settings.CONFIG_DIR, Settings.EXCLUDE_FILE) if not isfile(
            join(self.path, Settings.EXCLUDE_FILE)) else join(self.path, Settings.EXCLUDE_FILE)
        self.exclude_from = '--exclude-from={0}'.format(exc)
        self.path = join(self.path, name)

    def show(self):
        print('Path: {0}'.format(self.path))
        print('Host: {0}'.format(self.host))
        print('Options: {0} {1}'.format(Settings.RS_ARGS, self.exclude_from))


def callSync(lst):
    subprocess.call(['rsync'] + lst)
