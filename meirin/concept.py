import abc
import enum

# https://docs.python.org/zh-cn/3.11/library/enum.html

@enum.unique
class Decision(enum.Enum):
    """ Decision for Access Control System
    """

    PERMIT        = "permit"
    DENY          = "deny"
    INDETERMINATE = "indeterminate"
    NOTAPPLICABLE = "notapplicable"

    def __str__(self):
        return self.value

def parseDecision(string):
    """parse string to Decision Enum
    """
    for elem in Decision:
        if elem.value == string:
            return elem
    # raise ValueError("'{}' is not a vaild Decision".format(string))

class Context(abc.ABC):
    """ Context for Access Control System
    """
    @property
    @abc.abstractmethod
    def subject(self):
        pass

    @property
    @abc.abstractmethod
    def object(self):
        pass

    @property
    @abc.abstractmethod
    def action(self):
        pass

    @property
    @abc.abstractmethod
    def environment(self):
        pass
