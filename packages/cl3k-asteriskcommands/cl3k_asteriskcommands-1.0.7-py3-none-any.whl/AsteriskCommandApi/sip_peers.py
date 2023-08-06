import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class SIPpeers(AsteriskCommand):
    ActionID: str
    Action: str = "SIPpeers"
