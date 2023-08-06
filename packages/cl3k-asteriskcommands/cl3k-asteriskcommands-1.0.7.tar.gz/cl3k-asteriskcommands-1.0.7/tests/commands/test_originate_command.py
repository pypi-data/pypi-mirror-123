from unittest import TestCase
import json
from uuid import uuid4
from AsteriskCommandApi.originate import Originate
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_originate(self):
        action_id = str(uuid4())
        transaction_id = str(uuid4())

        command = Originate(
            ActionID=action_id,
            Channel="SIP/100",
            Context="Test",
            Exten="999",
            Priority="1",
            Callerid="10000",
            Timeout=30,
        )
        command.Variables = {
            "IDRegistro": "100",
            "CallActionID": transaction_id,
            "AgentCode": "999",
        }

        expected_dictionary = {
            "Variables": {"IDRegistro": "100", "CallActionID": transaction_id, "AgentCode": "999",},
            "ActionID": action_id,
            "Channel": "SIP/100",
            "Context": "Test",
            "Exten": "999",
            "Priority": "1",
            "Callerid": "10000",
            "Timeout": 30,
            "Action": "Originate",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: Originate
                ActionID: {action_id}
                Channel: SIP/100
                Context: Test
                Exten: 999
                Priority: 1
                Callerid: 10000
                Timeout: 30
                Variable: IDRegistro=100
                Variable: CallActionID={transaction_id}
                Variable: AgentCode=999
                """
            )
        )

        self.assertTrue(command.is_asterisk_command)
        self.assertDictEqual(command.as_dict(), expected_dictionary)
        self.assertEqual(command.as_json_asterisk_command(), json.dumps(expected_dictionary))
        self.assertEqual(str(command.as_asterisk_command()), expected_asterisk_command)
