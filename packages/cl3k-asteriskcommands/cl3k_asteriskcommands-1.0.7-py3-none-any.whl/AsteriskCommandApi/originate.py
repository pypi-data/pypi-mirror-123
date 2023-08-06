import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class Originate(AsteriskCommand):
    ActionID: str
    Channel: str
    Context: str
    Exten: str
    Priority: str
    Callerid: str
    Timeout: str
    Action: str = "Originate"
