from unittest import TestCase
from uuid import uuid4
from AsteriskCommandApi.set_var import SetVar
from tests.commands.auxiliar_commands import Auxiliar


class TestCommands(TestCase):
    def test_set_var(self):
        action_id = str(uuid4())

        asterisk_command = SetVar(
            ActionID=action_id, Channel="SIP/999", Variable="myVar", Value="myValue"
        )

        expected_dictionary = {
            "Action": "SetVar",
            "ActionID": action_id,
            "Channel": "SIP/999",
            "Variable": "myVar",
            "Value": "myValue",
        }

        expected_asterisk_command = Auxiliar.format_as_asterisk_command(
            str(
                f"""Action: SetVar
                ActionID: {action_id}
                Channel: SIP/999
                Variable: myVar
                Value: myValue
                """
            )
        )

        self.assertDictEqual(asterisk_command.as_dict(), expected_dictionary)
        self.assertEqual(
            str(asterisk_command.as_asterisk_command()), expected_asterisk_command
        )
        self.assertTrue(asterisk_command.is_asterisk_command)
