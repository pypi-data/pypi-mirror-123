from AsteriskCommandApi.originate import Originate
from AsteriskCommandApi.atxfer import Atxfer
from unittest import TestCase
from uuid import uuid4


class TestReceiveCommands(TestCase):
    def test_atxfer(self):
        action_id = str(uuid4())
        command_dictionary = {
            "Action": "Atxfer",
            "ActionID": action_id,
            "Channel": "SIP/123",
            "Context": "Test",
            "Exten": "SIP/111",
            "Priority": "1",
            "peerName": "1000",
        }

        asterisk_command = Atxfer(**command_dictionary)

        self.assertEqual(asterisk_command.ActionID, action_id)

    def test_originate(self):
        action_id = str(uuid4())
        transaction_id = str(uuid4())

        command_dictionary = {
            "Action": "Originate",
            "ActionID": action_id,
            "Channel": "SIP/100",
            "Context": "Test",
            "Exten": "999",
            "Priority": "1",
            "Callerid": "10000",
            "Timeout": 30,
            "Variables": {
                "IDRegistro": "100",
                "CallActionID": transaction_id,
                "AgentCode": "999",
            },
        }

        asterisk_command = Originate(**command_dictionary)

        self.assertEqual(asterisk_command.ActionID, action_id)
        self.assertEqual(asterisk_command.Variables["IDRegistro"], "100")
