import json
import subprocess

from platform.execute.local import local
from platform.execute.run import run
from platform.execute.ssh import ssh
from src.db.workspace import Workspace


class ArcSync(object):
    def __init__(self, dry, erase_missing, **kwargs):
        self.erase_missing = erase_missing
        self.dry = dry

    def options(self):
        return [
            f'erase_missing - {self.erase_missing}',
            f'dry - {self.dry}'
        ]

    def sync(self, source, dest, source_impl, dest_impl, source_host, dest_host):
        if not self.erase_missing:
            status = json.loads(
                run(impl=dest_impl, host=dest_host)
                    .withstderr()
                    .cmd(f'cd {dest} && arc status --json')
                    .call(p=True)
            )['status']

            if status in ['staged', 'changed', 'untracked', 'unmerged']:
                print(str(status))
                raise Exception('copy is not clean')

        info = json.loads(
            run(impl=source_impl, host=source_host)
                .withstderr()
                .cmd(f'cd {source} && arc info --json')
                .call(p=True)
        )

        print(str(info))

        if info['branch'] == 'trunk':
            raise Exception('wrong branch')

        if info['summary'] == '_RS_SYNC_COMMIT_' and not self.dry:
            msg = '--amend --no-edit'
        else:
            msg = '-m "_RS_SYNC_COMMIT_"'

        for s in run(impl=source_impl, host=source_host).withstderr()\
            .cmd(f'cd {source} && cd `arc root` && arc add --all && arc commit {msg}'
                 f' && arc push -f {info["branch"]}').exec():
            print(s)

        ff = f'''cd {dest} && cd `arc root` && arc fetch --all && \
test "$(arc info --json | ./ya tool jq '.branch' -r)" = "{info["branch"]}" && \
arc reset arcadia/users/massaraksh/{info["branch"]} --hard'''

        run(host=dest_host, impl=dest_impl).withstderr()\
            .cmd(ff)\
            .call(p=True, throw=True)

    def send(self, source, destination, ws: Workspace):
        self.sync(source=source, dest=destination.split(':')[1], source_host='localhost', dest_host=ws.host,
                  source_impl=local(), dest_impl=ssh())

    def get(self, source, destination, ws: Workspace):
        self.sync(source=source.split(':')[1], dest=destination, source_host=ws.host, dest_host='localhost',
                  source_impl=ssh(), dest_impl=local())


class RsyncSync(object):
    def __init__(self, args, exclude, dry, erase_missing):
        self._options = ['rsync'] + ['--exclude-from='+exclude, '--cvs-exclude'] + args
        if dry:
            self._options.append('-n')
        if erase_missing:
            self._options.append('--delete')

    def options(self):
        return self._options

    def get(self, source, destination, ws):
        self.sync(source=source, destination=destination)

    def send(self, source, destination, ws):
        self.sync(source=source, destination=destination, ws=ws)

    def sync(self, source, destination, ws: Workspace):
        subprocess.call(self._options + [source+'/', destination])
