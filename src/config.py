from src.settings import Settings
import json

class Config:
    def __init__(self):
        with open(Settings.CONFIG_FILE, 'r') as f:
            map = json.load(f)
            self.defaultWorkspace = map['defaultWorkspace']
            self.homeFolderName = map['homeFolderName']
            self.excludeFileName = map['excludeFileName']
            self.argSync = map['argSync']

    def serialize(self):
        with open(Settings.CONFIG_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=4, sort_keys=True)

    def print(self):
        print('Стандартное рабочее окружение')
        print('\tdefaultWorkspace: ' + self.defaultWorkspace)
        print('Название папки /home')
        print('\thomeFolderName: ' + self.homeFolderName)
        print('Название файла с несинхронизируемыми файлами')
        print('\texcludeFileName: ' + self.excludeFileName)
        print('Опции синхронизации')
        print('\targSync: ' + str(self.argSync))