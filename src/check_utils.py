from platform.exception import WrongTargets, WrongDelimers, WrongOptions
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

    @staticmethod
    def option(p: Params, option):
        if option not in p.options:
            raise WrongOptions('Ожидалась опция {0}, однако получено {1}'.format(option, str(p.options)))
        return True

    @staticmethod
    def inArray(arr, el, message = None):
        if el not in arr:
            m = 'Отсутсвует элемент {0}, получено {1}'.format(el, str(arr))
            raise ValueError(m if message is None else message)
        return True


class Check:
    @staticmethod
    def delimerType(delimer, type):
        if not isinstance(delimer, type):
            raise WrongDelimers('Неверный тип разделителя: получен {0}, ожидался {1}'
                                .format(delimer.__name__, type.__name__))
        return True

    @staticmethod
    def optionNamesInSet(p: Params, set):
        for o in p.options:
            if o not in set:
                raise WrongOptions('Опция {0} отсутствует в списке разрешённых: {1}'.format(o, str(p.options)))
        return True


class Empty:
    @staticmethod
    def options(p: Params):
        if p.options:
            raise WrongOptions('Опции должны быть пусты: {0}'.format(str(p.options)))
        return True

    @staticmethod
    def array(arr):
        if arr:
            raise ValueError('Массив должен быть пуст: {0}'.format(str(arr)))
        return True

    @staticmethod
    def delimers(p: Params):
        if p.delimer:
            raise WrongDelimers('Разделители должны быть пусты: {0}'.format(str(p.delimer)))
        return True

    @staticmethod
    def targets(p: Params):
        if p.targets:
            raise WrongTargets('Цели должны быть пусты: {0}'.format(str(p.targets)))
        return True


class NotEmpty:
    @staticmethod
    def options(p: Params):
        if not p.options:
            raise WrongOptions('Опции должны быть не пусты')
        return True

    @staticmethod
    def array(arr):
        if not arr:
            raise ValueError('Массив должен быть не пуст')
        return True

    @staticmethod
    def delimers(p: Params):
        if not p.delimer:
            raise WrongDelimers('Разделители должны быть не пусты')
        return True

    @staticmethod
    def targets(p: Params):
        if not p.targets:
            raise WrongTargets('Цели должны быть не пусты')
        return True


class Size:
    @staticmethod
    def equals(arr, size, message = None):
        if len(arr) != size:
            m = 'Неверный размер массива: ожидалось {0}, получен {1}'.format(len(arr), size)
            raise ValueError(m if not message else message)
        return True

    @staticmethod
    def notEquals(arr, size, message = None):
        if len(arr) == size:
            m = 'Неверный размер массива: ожидалось {0}, получен {1}'.format(len(arr), size)
            raise ValueError(m if not message else message)
        return True


def emptyCommand(func):
    return [lambda p: func if Empty.delimers(p) and
                              Empty.options(p) and
                              Empty.targets(p)
                       else raiseWrongParsing()]


def singleOptionCommand(res, functor = lambda p: True):
    return [lambda p: res if Empty.delimers(p) and
                             Empty.options(p) and
                             Size.equals(p.targets, 1) and
                             functor(p)
                      else raiseWrongParsing()]


def raiseWrongParsing():
    raise ValueError('Ошибочное условие')