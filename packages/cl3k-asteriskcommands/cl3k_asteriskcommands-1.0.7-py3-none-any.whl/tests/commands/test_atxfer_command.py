from unittest import TestCase
import json
from uuid import uuid4
from AsteriskCommandApi.atxfer import Atxfer
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_atxfer(self):
        action_id = str(uuid4())

        command = Atxfer(
            ActionID=action_id, Channel="SIP/123", Context="Test", Exten="SIP/111", Priority="1", peerName="1000",
        )

        expected_dictionary = {
            "ActionID": action_id,
            "Channel": "SIP/123",
            "Context": "Test",
            "Exten": "SIP/111",
            "Priority": "1",
            "peerName": "1000",
            "Action": "Atxfer",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: Atxfer
                ActionID: {action_id}
                Channel: SIP/123
                Context: Test
                Exten: SIP/111
                Priority: 1
                peerName: 1000
                """
            )
        )

        self.assertDictEqual(command.as_dict(), expected_dictionary)
        self.assertTrue(command.is_asterisk_command)
        self.assertEqual(str(command.as_asterisk_command()), expected_asterisk_command)
        self.assertEqual(command.as_json_asterisk_command(), json.dumps(expected_dictionary))
