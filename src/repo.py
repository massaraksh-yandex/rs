from src.settings import Settings
from os.path import basename
from os.path import join
from glob import glob
import sys

def getProjects(path = Settings.REMOTES_DIR):
    if path not in sys.path:
        sys.path.append(path)

    remotes = [ basename(dir) for dir in glob(join(path, '*.py')) ]
    return { name[:-3]: __import__(name[:-3], globals(), locals()).data for name in remotes }