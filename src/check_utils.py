from platform.exception import WrongTargets, WrongOptions
from platform.params import Params
from src.project import getProjects
from src.workspace import getWorkspaces


class NotExist:
    @staticmethod
    def projects(projectList):
        availableProjects = getProjects()
        for proj in projectList:
            if proj in availableProjects:
                raise WrongTargets('Проект {0} существует'.format(proj))
        return True

    @staticmethod
    def project(proj):
        return NotExist.projects([proj])

    @staticmethod
    def workspaces(wsList):
        for ws in wsList:
            if ws in getWorkspaces():
                raise WrongTargets('Рабочее окружение {0} существует'.format(ws))
        return True

    @staticmethod
    def workspace(ws):
        return NotExist.workspaces([ws])


class Exist:
    @staticmethod
    def projects(projectList):
        availableProjects = getProjects()
        for proj in projectList:
            if proj not in availableProjects:
                raise WrongTargets('Нет такого проекта: ' + proj)
        return True

    @staticmethod
    def project(proj):
        return Exist.projects([proj])

    @staticmethod
    def workspace(ws):
        return Exist.workspaces([ws])

    @staticmethod
    def workspaces(wsList):
        for ws in wsList:
            if ws not in getWorkspaces():
                raise WrongTargets('Нет такого рабочего окружения: ' + ws)
        return True
