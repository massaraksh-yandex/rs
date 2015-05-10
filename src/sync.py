import subprocess
from src.config import Config
from src.settings import Settings

class SyncData:
    path = None
    host = None
    remotePath = None
    excludeFile = None

    def __init__(self, path = '', host = '', remote = '', exclude = ''):
        self.path = path
        self.host = host
        self.remotePath = remote
        self.excludeFile = exclude

    def showSyncInfo(self):
        cfg = Config()
        print('Path: {0}'.format(self.path))
        print('Host: {0}'.format(self.host))
        print('Options: {0} {1}'.format(cfg.argSync, self.excludeFile))


def callSync(exclude, src, dest):
    cfg = Config()
    args = ['rsync', cfg.argSync, '--cvs-exclude', exclude, src, dest]
    subprocess.call(args)