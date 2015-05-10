from os.path import expanduser
from os.path import join


class Settings:
    CONFIG_DIR = expanduser('~/.rs')
    CONFIG_FILE = join(CONFIG_DIR, 'config.json')
    REMOTES_DIR = join(CONFIG_DIR, 'remotes')
    WORKSPACES_DIR = join(CONFIG_DIR, 'workspaces')
    EXCLUDE_FILE = 'rsignore'
    EXCLUDE_FROM = '--exclude-from=' + join(CONFIG_DIR, EXCLUDE_FILE)
    SYNC_ARGS = '-avcC'