__author__ = 'massaraksh'
from os import path
import os
from os.path import join
import re

def findAllFiles(path, regexp):
    return [join(top, obj) for top, dirs, files in os.walk(path) for obj in files if re.match(regexp, obj)]


def findAllDirs(path, regexp):
    return [join(top, obj) for top, dirs, files in os.walk(path) for obj in dirs if re.match(regexp, obj)]


def findAll(path, finder, types):
    ret = []
    for t in types:
        ret += finder(path, t)
    return ret


def createQtcreatorImportProject(name, full_path):
    def writeFile(name, path, content):
        with open(join(path, name), 'w') as f:
            f.writelines(content)

    def createFilesFile(name, path, content):
        writeFile(name+'.files', path, content)

    def createIncludesFile(name, path, content):
        writeFile(name+'.includes', path, content)

    def createConfigFile(name, path):
        writeFile(name+'.config', path, []) # empty file

    def createCreatorFile(name, path):
        writeFile(name+'.creator', path, ['[General]']) # empty file

    files = findAll(path, findAllFiles, ['*\.cpp', '*\.cxx', '*\.c\+\+', '*\.cc', '*\.c',
                                         '*\.hpp', '*\.hxx', '*\.hh', '*\.h'])

    directories = findAll(path, findAllDirs, ['*'])

    createFilesFile(name, path, files)
    createIncludesFile(name, path, directories)
    createConfigFile(name, path)
    createCreatorFile(name, path)


def createQmakeProject(name, full_path):
    def createProjectFile(name, path, sources, headers, dirs):
        with open(join(path, name+'.pro'), 'w') as f:
            f.write('TEMPLATE = aux')
            f.write('SOURCES += {0}')
            f.write('HEADERS += {0}')
            f.write('INCLUDEPATH += {0}')


    sources = findAll(path, findAllFiles, ['*\.cpp', '*\.cxx', '*\.c\+\+', '*\.cc', '*\.c'])
    headers = findAll(path, findAllFiles, ['*\.hpp', '*\.hxx', '*\.hh', '*\.h'])
    directories = findAll(path, findAllDirs, ['*'])

    createProjectFile(name, path, sources, headers, directories)
