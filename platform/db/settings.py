from os.path import join, expanduser


class Settings:
    def __init__(self, name = '.platform'):
        self._configdir = join(expanduser('~'), name)
        self._configfile = join(self.CONFIG_DIR, 'config.json')

    @property
    def CONFIG_DIR(self):
        return self._configdir

    @property
    def CONFIG_FILE(self):
        return self._configfile
