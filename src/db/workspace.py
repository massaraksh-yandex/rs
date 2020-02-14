import json


class Workspace:
    def __init__(self, name, host, path, sync_path, arc):
        self.name = name
        self.host = host
        self.path = path
        self.sync_path = sync_path
        self.arc = arc

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return '\n'.join(['Название: {name}',
                          'Хост: {host}',
                          'Корень: {path}',
                          'Чё синхрим: {sync_path}',
                          'Arc: {arc}',
                          ])\
            .format(**self.__dict__)
