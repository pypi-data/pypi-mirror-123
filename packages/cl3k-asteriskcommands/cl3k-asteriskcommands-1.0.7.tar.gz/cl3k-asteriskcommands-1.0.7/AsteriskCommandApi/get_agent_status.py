import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class GetAgentStatus(AsteriskCommand):
    ActionID: str
    Interface: str
    Action: str = "GetAgentStatus"
    is_asterisk_command: bool = False
