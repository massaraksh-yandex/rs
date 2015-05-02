from os.path import expanduser
from os.path import join


class Settings:
    CONFIG_DIR = expanduser('~/.rs')
    REMOTES_DIR = join(CONFIG_DIR, 'remotes')
    EXCLUDE_FILE = 'rsignore'
    EXCLUDE_FROM = '--exclude-from=' + join(CONFIG_DIR, EXCLUDE_FILE)
    RS_ARGS = '-avcC'

def getProjectPathByName(name):
    return join(Settings.REMOTES_DIR, name + '.json')
