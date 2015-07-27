from platform.db import database
from src.config import Config
from src.settings import Settings
from src.workspace import Workspace
from src.project import Project


class Database(database.Database):
    def __init__(self, config = Config()):
        super().__init__(config, Settings())

    def _getDirByType(self, type):
        if type == Project:
            return self.settings.REMOTES_DIR
        elif type == Workspace:
            return self.settings.WORKSPACES_DIR
        elif type == Config:
            return self.settings.CONFIG_DIR
        else:
            raise Exception('Неизвестный тип')

    def projects(self):
        return self.select('*', Project)

    def workspaces(self):
        return self.select('*', Workspace)


def initconfig():
    from platform.utils.utils import readLineWithPrompt
    from src.workspace import inputWorkspace
    name = readLineWithPrompt('Имя стандартного размещения', 'workspace')
    ws = inputWorkspace(name)
    if ws is None:
        print('Не могу продолжать без рабочего окружения')
        exit()

    map = {'defaultWorkspace': name,
           'homeFolderName': '/home',
           'excludeFileName': 'rsignore',
           'argSync': ['-avcC', '--out-format=%f -- %b %o']}

    db = Database(Config(map))
    db.update(db.config)