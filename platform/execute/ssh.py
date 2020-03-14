from subprocess import Popen, PIPE


class ssh(object):
    def _formparams(self, host, asShell, path, args):
        if asShell:
            return "ssh -T {0} 'cd {1} && {2}'".format(host, path, args)
        else:
            return ['ssh', '-T', host, 'cd {0} && '.format(path)] + args

    def cmd(self, err, host, path, args):
        shell = not isinstance(args, list)
        c = self._formparams(host, shell, path, args)
        return Popen(c, stdout=PIPE, stderr=err, shell=shell, bufsize=0)
