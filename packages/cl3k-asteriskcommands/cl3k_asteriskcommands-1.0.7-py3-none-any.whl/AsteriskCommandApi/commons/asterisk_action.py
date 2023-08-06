from typing import Iterable


class Action(object):
    def __init__(self, name, keys=None, variables=None):
        self.name = name
        self.keys = keys or dict()
        self.variables = variables or dict()

    def __str__(self):
        package = "Action: %s\r\n" % self.name
        for key in self.keys:
            if key != "Action" and key != "Variables" and key != "auxiliar_commands":
                package += "%s: %s\r\n" % (key, self.keys[key])
        if self.variables:
            lista_variables = ""
            separator = ""
            for var in self.variables:
                lista_variables += f"{separator}{var}={self.variables[var]}"
                separator = ","
            package += f"Variable: {lista_variables}"

        return package

    def __getattr__(self, item):
        return self.keys[item]

    def __setattr__(self, key, value):
        if key in ("name", "keys", "variables"):
            return object.__setattr__(self, key, value)
        self.keys[key] = value

    def __setitem__(self, key, value):
        self.variables[key] = value

    def __getitem__(self, item):
        return self.variables[item]
