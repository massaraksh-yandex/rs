from platform import config
from src.settings import Settings

class Config(config.Config):
    def __init__(self, m = None):
        super().__init__(map=m, settings=Settings())

    def __str__(self):
        s =  'Стандартное рабочее окружение\n'
        s += '\tdefaultWorkspace: ' + self.defaultWorkspace + '\n'
        s += 'Название папки /home\n'
        s += '\thomeFolderName: ' + self.homeFolderName + '\n'
        s += 'Название файла с несинхронизируемыми файлами\n'
        s += '\texcludeFileName: ' + self.excludeFileName + '\n'
        s += 'Опции синхронизации\n'
        s += '\targSync: ' + str(self.argSync) + '\n'
        return s

    @property
    def defaultWorkspace(self) -> str:
        return self.params['defaultWorkspace']

    @property
    def homeFolderName(self) -> str:
        return self.params['homeFolderName']

    @property
    def excludeFileName(self) -> str:
        return self.params['excludeFileName']

    @property
    def argSync(self) -> []:
        return self.params['argSync']

    @staticmethod
    def defaultConfig():
        map = {}
        map['defaultWorkspace'] = ''
        map['homeFolderName'] = '/home'
        map['excludeFileName'] = 'rsignore'
        map['argSync'] = ['-avcC', '--out-format=%f -- %b %o']
        return Config(map)