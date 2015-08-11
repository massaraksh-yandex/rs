from platform.params.exception import WrongTargets


class NotExist:
    def __init__(self, database):
        self.database = database

    def projects(self, projectList):
        availableProjects = self.database.projects()
        for proj in projectList:
            if proj in availableProjects:
                raise WrongTargets('Проект {0} существует'.format(proj))
        return True

    def project(self, proj):
        return self.projects([proj])

    def workspaces(self, wsList):
        for ws in wsList:
            if ws in self.database.workspaces():
                raise WrongTargets('Рабочее окружение {0} существует'.format(ws))
        return True

    def workspace(self, ws):
        return self.workspaces([ws])


class Exist:
    def __init__(self, database):
        self.database = database

    def projects(self, projectList):
        availableProjects = self.database.projects()
        for proj in projectList:
            if proj not in availableProjects:
                raise WrongTargets('Нет такого проекта: ' + proj)
        return True

    def project(self, proj):
        return self.projects([proj])

    def workspace(self, ws):
        return self.workspaces([ws])

    def workspaces(self, wsList):
        for ws in wsList:
            if ws not in self.database.workspaces():
                raise WrongTargets('Нет такого рабочего окружения: ' + str(ws))
        return True
