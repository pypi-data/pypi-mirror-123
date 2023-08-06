import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class QueueAdd(AsteriskCommand):
    ActionID: str
    Queue: str
    Interface: str
    Penalty: str
    Paused: str
    MemberName: str
    StateInterface: str
    Action: str = "QueueAdd"
