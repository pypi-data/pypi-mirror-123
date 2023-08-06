import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class Queues(AsteriskCommand):
    ActionID: str
    Action: str = "Queues"
