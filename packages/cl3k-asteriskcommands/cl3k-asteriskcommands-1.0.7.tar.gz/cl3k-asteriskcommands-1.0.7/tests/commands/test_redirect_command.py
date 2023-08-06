from unittest import TestCase
from uuid import uuid4
from tests.commands.auxiliar_commands import Auxiliar
from AsteriskCommandApi.redirect import Redirect
from AsteriskCommandApi.set_var import SetVar
from AsteriskCommandApi.queue_pause import QueuePause


class TestCommands(TestCase):
    def test_redirect(self):
        action_id = str(uuid4())

        asterisk_command = Redirect(
            ActionID=action_id, Context="redirect", Exten="123", Priority="1", Channel="SIP/999", peerName="SIP/888",
        )

        expected_dictionary = {
            "Action": "Redirect",
            "ActionID": action_id,
            "Context": "redirect",
            "Exten": "123",
            "Priority": "1",
            "Channel": "SIP/999",
            "peerName": "SIP/888",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: Redirect
                ActionID: {action_id}
                Channel: SIP/999
                Context: redirect
                Exten: 123
                Priority: 1
                peerName: SIP/888
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(str(asterisk_command.as_asterisk_command()), expected_asterisk_command)
        self.assertTrue(asterisk_command.is_asterisk_command)

    def test_redirect_command_with_auxiliar_commands(self):
        action_id = str(uuid4())
        setvar_command = SetVar(ActionID=action_id, Channel="SIP/100", Variable="agentName", Value="1000")
        queue_pause_command = QueuePause(
            ActionID=action_id, Queue="ventas", Interface="SIP/100", Paused=False, Reason="100001", MemberName="1000",
        )

        redirect_command = Redirect(
            ActionID=action_id, Channel="SIP/100", Context="transfer", Exten="123", Priority="1", peerName="SIP/999",
        )

        redirect_command.auxiliar_commands.append(setvar_command.as_dict())
        redirect_command.auxiliar_commands.append(queue_pause_command.as_dict())

        expected_dictionary = {
            "auxiliar_commands": [
                {
                    "ActionID": action_id,
                    "Channel": "SIP/100",
                    "Variable": "agentName",
                    "Value": "1000",
                    "Action": "SetVar",
                },
                {
                    "ActionID": action_id,
                    "Queue": "ventas",
                    "Interface": "SIP/100",
                    "Paused": False,
                    "Reason": "100001",
                    "MemberName": "1000",
                    "Action": "QueuePause",
                },
            ],
            "ActionID": action_id,
            "Channel": "SIP/100",
            "Context": "transfer",
            "Exten": "123",
            "Priority": "1",
            "peerName": "SIP/999",
            "Action": "Redirect",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: Redirect
                ActionID: {action_id}
                Channel: SIP/100
                Context: transfer
                Exten: 123
                Priority: 1
                peerName: SIP/999
                """
            )
        )

        self.assertDictEqual(redirect_command.as_dict(), expected_dictionary)
        self.assertEqual(str(redirect_command.as_asterisk_command()), expected_asterisk_command)
        self.assertTrue(redirect_command.is_asterisk_command)
