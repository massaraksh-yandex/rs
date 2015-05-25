import subprocess
import sys
from platform.endpoint import Endpoint
from platform.params import Params
from platform.utils import makeCommandDict
from src.check_utils import singleOptionCommand, emptyCommand


class Gdb(Endpoint):
    def name(self):
        return 'gdb'

    def _help(self):
        return ['{path}']

    def _rules(self):
        return [lambda p: self.do]

    def do(self, p: Params):
        command = 'cd ~/ws/src/macs_pg/utils; gdb get_first_envelope_date'
        proc = subprocess.Popen(['ssh', 'wmidevaddr', command], stdout=sys.stdout, stderr=sys.stderr)
        while proc.poll() is None:
            pass


module_commands = makeCommandDict([Gdb])