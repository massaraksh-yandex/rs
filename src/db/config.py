from platform.db import config
from src.db.settings import Settings

class Config(config.Config):
    def __init__(self, m = None):
        super().__init__(map=m, settings=Settings())

    def __str__(self):
        return '\n'.join(['Стандартное рабочее окружение',
                          '\tdefaultWorkspace: {defaultWorkspace}',
                          'Название папки /home',
                          '\thomeFolderName: {homeFolderName}',
                          'Название файла с несинхронизируемыми файлами',
                          '\texcludeFileName: {excludeFileName}',
                          'Опции синхронизации',
                          '\targSync: {argSync}']).format(**self.params)

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
