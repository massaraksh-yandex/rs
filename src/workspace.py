from os.path import join
from platform.utils.utils import readLineWithPrompt
import json


class Workspace:
    def __init__(self, name, host, path, include, src, etc):
        self.name = name
        self.host = host
        self.path = path
        self.include = include
        self.src = src
        self.etc = etc

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return '\n'.join(['Название: {name}',
                          'Хост: {host}',
                          'Корень: {path}',
                          'Заголовочные файлы: {include}',
                          'Исходный код: {src}',
                          'Конфигурационные файлы: {etc}'])\
            .format(**self.__dict__)


def inputWorkspace(name):
    host = readLineWithPrompt('Хост', 'wmidevaddr')
    path = readLineWithPrompt('Путь', '~/ws')
    include = readLineWithPrompt('Заголовочные файлы', join(path, 'include'))
    src = readLineWithPrompt('Исходный код', join(path, 'src'))
    etc = readLineWithPrompt('Конфигурационные файлы', join(path, 'etc'))

    ws = Workspace(name, host, path, include, src, etc)
    if readLineWithPrompt('Всё верно (yes/no)', 'no') != 'yes':
        return None
    else:
        return ws
