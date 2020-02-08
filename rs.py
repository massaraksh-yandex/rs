#!/usr/local/bin/python3.7 -u
from platform.utils.main import main, ConfigHooks
from src.db.database import Database, initconfig
from src.db.settings import validatefiles, createfiles

if __name__ == '__main__':
    hooks = ConfigHooks(checkfiles=validatefiles, createfiles=createfiles,
                        saveconfig=initconfig, createdatabase=lambda: Database())
    main('rs', ['{path} - программа для синхронизации кода и удалённой сборки'], hooks)
