import subprocess


class RsyncSync(object):
    def __init__(self, args, exclude, dry, erase_missing):
        self._options = ['rsync'] + ['--exclude-from='+exclude, '--cvs-exclude'] + args
        if dry:
            self._options.append('-n')
        if erase_missing:
            self._options.append('--delete')


    def options(self):
        return self._options

    def sync(self, source, destination):
        subprocess.call(self._options + [source+'/', destination])
