from platform.db import database
from src.workspace import Workspace
from src.project import Project


class Database(database.Database):
    def _getDirByType(self, type):
        if type == Project:
            return self._settings.REMOTES_DIR
        elif type == Workspace:
            return self._settings.WORKSPACES_DIR
        else:
            raise Exception('Неизвестный тип')

    def projects(self):
        return self.select('*', Project)

    def workspaces(self):
        return self.select('*', Workspace)
