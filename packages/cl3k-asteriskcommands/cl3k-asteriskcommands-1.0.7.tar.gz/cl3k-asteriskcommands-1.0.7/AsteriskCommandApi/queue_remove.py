import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class QueueRemove(AsteriskCommand):
    ActionID: str
    Queue: str
    Interface: str
    Action: str = "QueueRemove"
