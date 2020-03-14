class Delimer(object):
    def __init__(self, index):
        self.index = index


class DoubleDelimer(Delimer):
    value = '--'


class SingleDelimer(Delimer):
    value = '-'
