import json


class Project:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.tests = kwargs['tests']
        self.path = kwargs['path']
        self.workspace = kwargs['ws']
        self.additional_build = kwargs['additional_build']
        self.additional_tests = kwargs['additional_tests']

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return '\n'.join(['Название: {name}',
                          'Путь: {path}',
                          'Тесты: {tests}',
                          'Дополнительные билды: {additional_build}',
                          'Дополнительные тесты: {additional_tests}',
                          'Рабочее окружение: {workspace}'])\
            .format(**self.__dict__)
