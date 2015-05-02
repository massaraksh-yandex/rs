from sys import stdout, stdin

__author__ = 'massaraksh'


def readLineWithPrompt(message, default):
    stdout.write('{0} [{1}]: '.format(message, default))
    line = stdin.readline().rstrip()
    if len(line) != 0:
        return line
    else:
        return default