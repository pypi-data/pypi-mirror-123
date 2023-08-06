import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class QueuePause(AsteriskCommand):
    ActionID: str
    Queue: str
    Interface: str
    Paused: str
    Reason: str
    MemberName: str
    Action: str = "QueuePause"
