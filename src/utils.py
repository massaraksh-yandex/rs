from os.path import join, isfile, expanduser
from src.config import Config
from src.settings import Settings


def readLineWithPrompt(message, default):
    line = input('{0} [{1}]: '.format(message, default)).rstrip()
    if len(line) != 0:
        return line
    else:
        return default


def getProjectPathByName(name):
    return join(Settings().REMOTES_DIR, name + '.json')

def getWorkspacePathByName(name):
    return join(Settings().WORKSPACES_DIR, name + '.json')

def getExcludeFileArg(path):
    cfg = Config()
    fileName = expanduser(join(path, cfg.excludeFileName))
    file = fileName if isfile(fileName) else Settings().CONFIG_DIR

    return '--exclude-from={0}'.format(file)


