from os.path import join, isfile
from sys import stdout, stdin

from src.settings import Settings


def readLineWithPrompt(message, default):
    stdout.write('{0} [{1}]: '.format(message, default))
    line = stdin.readline().rstrip()
    if len(line) != 0:
        return line
    else:
        return default


def getProjectPathByName(name):
    return join(Settings.REMOTES_DIR, name + '.json')

def getWorkspacePathByName(name):
    return join(Settings.WORKSPACES_DIR, name + '.json')

def getExcludeFile(path):
    if not isfile(join(path, Settings.EXCLUDE_FILE)):
        file = join(Settings.CONFIG_DIR, Settings.EXCLUDE_FILE)
    else:
        file = join(path, Settings.EXCLUDE_FILE)
    return '--exclude-from={0}'.format(file)


