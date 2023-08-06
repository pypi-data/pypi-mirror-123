from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.clear_idle_call_actors import ClearIdleCallActors
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_clear_idle_call_actors(self):
        action_id = str(uuid4())

        asterisk_command = ClearIdleCallActors(ActionID=action_id)

        expected_dictionary = {
            "ActionID": action_id,
            "Action": "ClearIdleCallActors",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: ClearIdleCallActors
                ActionID: {action_id}
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertFalse(asterisk_command.is_asterisk_command)
