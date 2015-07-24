from os.path import join
from platform.db import settings


class Settings(settings.Settings):
    def __init__(self):
        super().__init__('.rs')
        self._remotesdir = join(self.CONFIG_DIR, 'remotes')
        self._workspacesdir = join(self.CONFIG_DIR, 'workspaces')

    @property
    def REMOTES_DIR(self):
        return self._remotesdir

    @property
    def WORKSPACES_DIR(self):
        return self._workspacesdir


def validatefiles():
    from os.path import isdir, isfile
    s = Settings()
    return isdir(s.CONFIG_DIR) and isdir(s.REMOTES_DIR) and \
           isdir(s.WORKSPACES_DIR) and isfile(s.CONFIG_FILE)


def createfiles():
    from os import makedirs
    from src.utils import readLineWithPrompt

    answer = readLineWithPrompt('Создать конфиги в ~/.rs? [yes/no]', 'no')
    if answer != 'yes':
        exit()

    s = Settings()
    makedirs(s.CONFIG_DIR, exist_ok=True)
    makedirs(s.REMOTES_DIR, exist_ok=True)
    makedirs(s.WORKSPACES_DIR, exist_ok=True)
    with open(s.CONFIG_FILE, 'w') as f:
        f.write('{}')
