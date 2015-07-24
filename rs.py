#!/usr/local/bin/python3.4 -u
from platform.utils.main import main, ConfigHooks
from src.config import Config, initconfig
from src.settings import validatefiles, createfiles

if __name__ == '__main__':
    hooks = ConfigHooks(check=validatefiles, init=createfiles,
                        save=initconfig, create=lambda: Config())
    main('rs', ['{path} - программа для синхронизации кода и удалённой сборки'], hooks)
