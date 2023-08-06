import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class Redirect(AsteriskCommand):
    ActionID: str
    Channel: str
    Context: str
    Exten: str
    Priority: str
    peerName: str
    Action: str = "Redirect"
