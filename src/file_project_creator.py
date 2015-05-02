__author__ = 'massaraksh'
from os import path

def findAllImpl(path, regexp, direcroty):
    return []


def findAllFiles(path, regexp):
    return findAllImpl(path, regexp, False)


def findAllDirs(path, regexp):
    return findAllImpl(path, regexp, True)


def findAll(path, finder, types):
    ret = []
    for t in types:
        finder(path, t)
    return ret


def createQtcreatorImportProject(name, full_path):
    def createFilesFile(name, path, content):
        pass

    def createIncludesFile(name, path, content):
        pass

    def createConfigFile(name, path):
        pass  # empty

    def createCreatorFile(name, path):
        pass  # just [General]

    files = findAll(path, findAllFiles, ['*.cpp', '*.cxx', '*.cc', '*.c',
                                         '*.hpp', '*.hxx', '*.hh', '*.h'])

    direcroties = findAll(path, findAllDirs, ['*'])

    createFilesFile(name, path, files)
    createIncludesFile(name, path, direcroties)
    createConfigFile(name, path)
    createCreatorFile(name, path)


def createQmakeProject(name, full_path):
    def createProjectFile(name, path, sources, headers, dirs):
        pass  # TEMPLATE = aux

    sources = findAll(path, findAllFiles, ['*.cpp', '*.cxx', '*.cc', '*.c'])
    headers = findAll(path, findAllFiles, ['*.hpp', '*.hxx', '*.hh', '*.h'])
    direcroties = findAll(path, findAllDirs, ['*'])

    createProjectFile(name, path, sources, headers, direcroties)
