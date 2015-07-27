#!/usr/local/bin/python3.4 -u
from platform.utils.main import main, ConfigHooks
from src.database import Database, initconfig
from src.settings import validatefiles, createfiles

if __name__ == '__main__':
    hooks = ConfigHooks(checkfiles=validatefiles, createfiles=createfiles,
                        saveconfig=initconfig, createdatabase=lambda: Database())
    main('rs', ['{path} - программа для синхронизации кода и удалённой сборки'], hooks)
