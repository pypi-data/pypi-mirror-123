import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class SetVar(AsteriskCommand):
    ActionID: str
    Channel: str
    Variable: str
    Value: str
    Action: str = "SetVar"
