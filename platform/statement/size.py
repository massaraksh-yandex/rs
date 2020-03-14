from platform.params.exception import PlatformException


class Size:
    def __init__(self, rule):
        self.rule = rule

    def equals(self, arr, size):
        if len(arr) != size:
            raise PlatformException()
        return self.rule

    def moreOrEquals(self, arr, size):
        if len(arr) < size:
            raise PlatformException()
        return self.rule

    def notEquals(self, arr, size):
        if len(arr) == size:
            raise PlatformException()
        return self.rule
