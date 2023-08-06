from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.hangup import Hangup
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_hangup(self):
        action_id = str(uuid4())

        asterisk_command = Hangup(
            ActionID=action_id, Channel="SIP/999", peerName="1000"
        )

        expected_dictionary = {
            "Action": "Hangup",
            "ActionID": action_id,
            "Channel": "SIP/999",
            "peerName": "1000",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: Hangup
                ActionID: {action_id}
                Channel: SIP/999
                peerName: 1000
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertTrue(asterisk_command.is_asterisk_command)
