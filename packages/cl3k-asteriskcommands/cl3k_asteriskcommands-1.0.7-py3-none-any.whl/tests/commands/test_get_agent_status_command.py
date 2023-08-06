from typing import Iterable
from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.get_agent_status import GetAgentStatus
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_get_agent_status(self):
        action_id = str(uuid4())

        asterisk_command = GetAgentStatus(ActionID=action_id, Interface="SIP/999")

        expected_dictionary = {
            "Action": "GetAgentStatus",
            "ActionID": action_id,
            "Interface": "SIP/999",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: GetAgentStatus
                ActionID: {action_id}
                Interface: SIP/999
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertFalse(asterisk_command.is_asterisk_command)
