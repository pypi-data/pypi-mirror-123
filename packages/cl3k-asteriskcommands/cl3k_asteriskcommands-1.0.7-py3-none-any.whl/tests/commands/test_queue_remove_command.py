from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.queue_remove import QueueRemove
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_queue_remove(self):
        action_id = str(uuid4())

        asterisk_command = QueueRemove(
            ActionID=action_id,
            Queue="ventas",
            Interface="SIP/999",
        )

        expected_dictionary = {
            "Action": "QueueRemove",
            "ActionID": action_id,
            "Queue": "ventas",
            "Interface": "SIP/999",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: QueueRemove
                ActionID: {action_id}
                Queue: ventas
                Interface: SIP/999
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertTrue(asterisk_command.is_asterisk_command)
