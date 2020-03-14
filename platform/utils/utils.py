from os.path import join, basename
from glob import glob
import sys
import io


def importCommands(path):
    commandsPath = join(path, 'commands')
    sys.path.append(commandsPath)
    commands = {}
    for name in glob(commandsPath + '/*.py'):
        module = __import__(basename(name[:-3]), globals(), locals())

        try:
            for command in module.commands.keys():
                commands[command] = module.commands[command]
        except AttributeError:
            pass

    return commands


def registerCommands(*commands):
    return { c.name(c): c for c in commands }


def setupCodecs():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering = True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering = True)
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


def readLineWithPrompt(message, default):
    line = input('{0} [{1}]: '.format(message, default)).rstrip()
    if len(line) != 0:
        return line
    else:
        return default