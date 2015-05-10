import json
from src.settings import Settings

class Config:
    defaultWorkspace = ''
    homeFolderName = ''

    def __init__(self):
        with open(Settings.CONFIG_FILE, 'r') as f:
            map = json.load(f)
            self.defaultWorkspace = map['defaultWorkspace']
            self.homeFolderName = map['homeFolderName']

    def serialize(self):
        with open(Settings.CONFIG_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=4, sort_keys=True)

    def print(self):
        print('Стандартное рабочее окружение: ' + self.defaultWorkspace)
        print('Название папки /home: ' + self.homeFolderName)