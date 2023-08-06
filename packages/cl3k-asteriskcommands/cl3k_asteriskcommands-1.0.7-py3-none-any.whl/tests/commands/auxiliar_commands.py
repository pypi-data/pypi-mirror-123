import re


class Auxiliar:
    @staticmethod
    def format_as_asterisk_command(asterisk_command: str) -> str:
        result = asterisk_command.replace("\n", "\r\n")
        return re.sub("[ ]{2,}", "", result)
