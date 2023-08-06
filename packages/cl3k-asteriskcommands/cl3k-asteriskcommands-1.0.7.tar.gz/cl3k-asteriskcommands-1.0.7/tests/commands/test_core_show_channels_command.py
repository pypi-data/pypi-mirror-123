from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.core_show_channels import CoreShowChannels
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_core_show_channels(self):
        action_id = str(uuid4())

        asterisk_command = CoreShowChannels(ActionID=action_id)

        expected_dictionary = {
            "Action": "CoreShowChannels",
            "ActionID": action_id,
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: CoreShowChannels
                ActionID: {action_id}
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertTrue(asterisk_command.is_asterisk_command)
