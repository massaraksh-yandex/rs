from os.path import join, isfile
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
    path = path if isfile(join(path, cfg.excludeFileName)) else Settings().CONFIG_DIR
    file = join(path, cfg.excludeFileName)

    return '--exclude-from={0}'.format(file)


