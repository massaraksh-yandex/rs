from subprocess import Popen, PIPE


class local(object):
    def _formparams(self, asShell, path, args):
        if asShell:
            return 'cd {0} && {1}'.format(path, args)
        else:
            return ['cd {0} && '.format(path)] + args

    def cmd(self, err, host, path, args):
        shell = not isinstance(args, list)
        p = self._formparams(shell, path, args)
        print(str(p))
        return Popen(p, stdout=PIPE, stderr=err, shell=shell, bufsize=0)
