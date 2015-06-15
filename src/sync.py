import subprocess
from src.config import Config

class SyncData:
    def __init__(self, path = '', host = '', remote = '', exclude = ''):
        self.path = path
        self.host = host
        self.remotePath = remote
        self.excludeFile = exclude

    def showSyncInfo(self):
        cfg = Config()
        print('Path: {0}'.format(self.path))
        print('Host: {0}'.format(self.host))
        print('Options: {0} {1}'.format(' '.join(cfg.argSync), self.excludeFile))


def callSync(exclude, src, dest, dryRun = False):
    cfg = Config()
    args = ['rsync'] + cfg.argSync
    if dryRun:
        args.append('-n')
    args = args + ['--cvs-exclude', exclude, src, dest]
    subprocess.call(args)