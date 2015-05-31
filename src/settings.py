from platform import settings
from os.path import join


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