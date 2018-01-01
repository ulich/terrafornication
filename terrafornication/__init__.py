import json
import collections
from provider import Provider

class Terrafornication:

    def __init__(self):
        self.variables = {}
        self.providers = []
        self.resources = {}
        self.data_sources = {}


    def variable(self, name, properties):
        if name in self.variables:
            raise DuplicateVariableException("The variable {} already exists".format(name))

        self.variables[name] = properties
        return Variable(name)
    

    def provider(self, type, properties):
        p = Provider(type, properties, self.resources, self.data_sources)
        self.providers.append(p)
        return p


    def to_dict(self):
        return {
            "variable": self.variables,
            "provider": self._to_provider_dict(),
            "data": self.data_sources,
            "resource": self.resources
        }


    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


    def _to_provider_dict(self):
        return map(lambda p: { p.type: p.properties }, self.providers)


class Variable:
    
    def __init__(self, name):
        self.name = name

    def ref(self):
        return "${{var.{}}}".format(self.name)


class DuplicateVariableException(RuntimeError):
    pass
