import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class SIPpeerstatus(AsteriskCommand):
    ActionID: str
    Action: str = "SIPpeerstatus"
