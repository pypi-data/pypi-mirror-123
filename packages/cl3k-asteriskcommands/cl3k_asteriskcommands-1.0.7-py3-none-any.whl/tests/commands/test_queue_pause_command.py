from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.queue_pause import QueuePause
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_queue_pause(self):
        action_id = str(uuid4())

        asterisk_command = QueuePause(
            ActionID=action_id,
            Queue="ventas",
            Interface="SIP/999",
            Paused=False,
            Reason="100001",
            MemberName="1000",
        )

        expected_dictionary = {
            "Action": "QueuePause",
            "ActionID": action_id,
            "Queue": "ventas",
            "Interface": "SIP/999",
            "Paused": False,
            "Reason": "100001",
            "MemberName": "1000",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: QueuePause
                ActionID: {action_id}
                Queue: ventas
                Interface: SIP/999
                Paused: False
                Reason: 100001
                MemberName: 1000
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertTrue(asterisk_command.is_asterisk_command)
