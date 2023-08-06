import attr
import json
from typing import Dict
from AsteriskCommandApi.commons.asterisk_action import Action


@attr.s(kw_only=True)
class AsteriskCommand:
    Action = attr.ib(default="")
    ActionID = attr.ib(default="")
    auxiliar_commands = attr.ib(default=attr.Factory(list))
    Variables = attr.ib(default=attr.Factory(dict))
    is_asterisk_command = attr.ib(default=attr.Factory(bool, True))

    def as_dict(self) -> Dict:
        return attr.asdict(
            self,
            filter=lambda attr, value: (isinstance(value, (dict, list)) and bool(value))
            or (not isinstance(value, (dict, list)))
            and attr.name != "is_asterisk_command",
        )

    def as_json_asterisk_command(self) -> str:
        return json.dumps(self.as_dict())

    def as_asterisk_command(self) -> Action:
        return Action(name=self.Action, keys=self.as_dict(), variables=self.Variables)
