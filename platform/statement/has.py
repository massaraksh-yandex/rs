from platform.params.exception import WrongOptions, PlatformException


class Has:
    def __init__(self, rule):
        self.rule = rule
        self.p = rule.params

    def option(self, option):
        if option not in self.p.options:
            raise WrongOptions()
        return self.rule

    def inArray(self, arr, el):
        if el not in arr:
            raise PlatformException()
        return self.rule