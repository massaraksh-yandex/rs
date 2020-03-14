from platform.params.exception import WrongDelimers, WrongOptions, WrongTargets


class Check:
    def __init__(self, rule):
        self.rule = rule
        self.p = rule.params

    def delimersType(self, type):
        for d in self.p.delimers:
            if not isinstance(d, type):
                raise WrongDelimers()
        return self.rule

    def optionNamesInSet(self, *set):
        for o in self.p.options:
            if o not in set:
                raise WrongOptions()
        return self.rule

    def optionValueInSet(self, name, *set):
        value = self.p.options[name]
        if not value and None not in set:
            raise WrongOptions()
        if value not in set:
            raise WrongOptions()
        return self.rule

    def target(self, index, pattern):
        if self.p.targets[index].value != pattern:
            raise WrongTargets()
        return self.rule