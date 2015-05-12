from platform.exception import WrongTargets, WrongDelimers, WrongOptions
from platform.params import Params
from src.project import getProjects


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


class Check:
    @staticmethod
    def delimerType(delimer, type):
        if not isinstance(delimer, type):
            raise WrongDelimers('Неверный тип разделителя: получен {0}, ожидался {1}'
                                .format(delimer.__name__, type.__name__))
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


def raiseWrongParsing():
    raise ValueError('Ошибочное условие')