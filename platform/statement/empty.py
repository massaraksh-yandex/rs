from platform.params.exception import WrongOptions, PlatformException, WrongDelimers, WrongTargets


class Empty:
    def __init__(self, rule):
        self.rule = rule
        self.p = rule.params

    def options(self):
        if self.p.options:
            raise WrongOptions()
        return self.rule

    def array(self, arr):
        if arr:
            raise PlatformException()
        return self.rule

    def delimers(self):
        if self.p.delimers:
            raise WrongDelimers()
        return self.rule

    def targets(self):
        if self.p.targets:
            raise WrongTargets()
        return self.rule