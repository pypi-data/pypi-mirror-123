import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class GetInfoAnexos(AsteriskCommand):
    ActionID: str
    Action: str = "GetInfoAnexos"
    is_asterisk_command: bool = False
