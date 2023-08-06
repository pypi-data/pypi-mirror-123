from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.queue_status import QueueStatus
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_queue_status(self):
        action_id = str(uuid4())

        asterisk_command = QueueStatus(
            ActionID=action_id,
        )

        expected_dictionary = {
            "Action": "QueueStatus",
            "ActionID": action_id,
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: QueueStatus
                ActionID: {action_id}
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertTrue(asterisk_command.is_asterisk_command)
