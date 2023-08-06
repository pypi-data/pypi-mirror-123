from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.get_info_anexos import GetInfoAnexos
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_get_info_anexos(self):
        action_id = str(uuid4())

        asterisk_command = GetInfoAnexos(ActionID=action_id)

        expected_dictionary = {
            "Action": "GetInfoAnexos",
            "ActionID": action_id,
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: GetInfoAnexos
                ActionID: {action_id}
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertFalse(asterisk_command.is_asterisk_command)
