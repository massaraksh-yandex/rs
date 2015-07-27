def readLineWithPrompt(message, default):
    line = input('{0} [{1}]: '.format(message, default)).rstrip()
    if len(line) != 0:
        return line
    else:
        return default


