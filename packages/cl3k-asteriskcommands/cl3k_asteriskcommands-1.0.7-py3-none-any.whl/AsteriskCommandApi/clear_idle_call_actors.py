import attr
from AsteriskCommandApi.commons.asterisk_command import AsteriskCommand


@attr.s(auto_attribs=True)
class ClearIdleCallActors(AsteriskCommand):
    ActionID: str
    Action: str = "ClearIdleCallActors"
    is_asterisk_command: bool = False
