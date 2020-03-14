from platform.params.params import Params
from platform.statement.check import Check
from platform.statement.empty import Empty
from platform.statement.has import Has
from platform.statement.notempty import NotEmpty
from platform.statement.size import Size


class Rule:
    def __init__(self, p: Params):
        self.params = p

    def size(self):
        return Size(self)

    def check(self):
        return Check(self)

    def empty(self):
        return Empty(self)

    def notEmpty(self):
        return NotEmpty(self)

    def has(self):
        return Has(self)


