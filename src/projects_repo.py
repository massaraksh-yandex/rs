from src.settings import Settings
from os.path import basename
from os.path import join
from glob import glob
from sys import path


class Repo:
    projects = None

    @staticmethod
    def parse():
        path.append(Settings.REMOTES_DIR)
        remotes = [ basename(dir) for dir in glob(join(Settings.REMOTES_DIR, '*.py')) ]
        Repo.projects = { name[:-3]: __import__(name[:-3], globals(), locals()).data for name in remotes }