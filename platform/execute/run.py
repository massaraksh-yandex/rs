from subprocess import STDOUT

from platform.execute.ssh import ssh


class run(object):
    def __init__(self, host = 'localhost', impl = ssh()):
        self._host = host
        self._args = []
        self._stderr = None
        self._path = '.'
        self._impl = impl

    def cmd(self, s):
        self._args = s
        return self

    def withstderr(self):
        self._stderr = STDOUT
        return self

    def path(self, p):
        self._path = p
        return self

    def call(self, p=False, throw=False):
        pid = self._impl.cmd(self._stderr, self._host, self._path, self._args)
        s = pid.communicate()[0].decode('utf-8')
        if p:
            print(s)
        if throw and pid.returncode != 0:
            raise Exception(str(self._args))
        return s

    def exec(self):
        p = self._impl.cmd(self._stderr, self._host, self._path, self._args)
        while True:
            line = p.stdout.readline().decode('utf-8')
            if line == '':
                break
            yield line