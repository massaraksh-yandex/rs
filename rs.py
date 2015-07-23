#!/usr/local/bin/python3.4 -u
from platform import utils
from src.config import Config, initconfig
from src.settings import validatefiles, createfiles

if __name__ == "__main__":
    hooks = utils.ConfigHooks(check=validatefiles, init=createfiles,
                              save=initconfig, create=lambda: Config())
    utils.main('rs', hooks)
