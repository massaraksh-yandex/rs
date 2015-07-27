from platform.db import database
from src.workspace import Workspace
from src.project import Project


class Database(database.Database):
    def _getDirByType(self, object):
        if isinstance(object, Project):
            return self._settings.REMOTES_DIR
        elif isinstance(object, Workspace):
            return self._settings.WORKSPACES_DIR
        else:
            raise Exception('Неизвестный тип')

    def projects(self):
        return self._selectAll(self._settings.REMOTES_DIR, Project)

    def workspaces(self):
        return self._selectAll(self._settings.WORKSPACES_DIR, Workspace)
