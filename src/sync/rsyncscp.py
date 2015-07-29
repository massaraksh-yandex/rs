import subprocess


class RsyncSync(object):
    def __init__(self, args, exclude, dry):
        self._options = ['rsync'] + ['--cvs-exclude', '--exclude-from='+exclude] + args
        if dry:
            self._options.append('-n')


    def options(self):
        return self._options

    def sync(self, source, destination):
        subprocess.call(self._options + [source+'/', destination])