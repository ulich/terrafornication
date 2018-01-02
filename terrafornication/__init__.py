from __future__ import absolute_import
import json
import collections
from . import provider

class Terrafornication:

    def __init__(self):
        self.variables = {}
        self.providers = []
        self.resources = {}
        self.data_sources = {}
        self.outputs = {}


    def variable(self, name, properties):
        if name in self.variables:
            raise DuplicateVariableException("The variable {0} already exists".format(name))

        self.variables[name] = properties
        return Variable(name)
    

    def provider(self, type, properties):
        p = provider.Provider(type, properties, self.resources, self.data_sources)
        self.providers.append(p)
        return p

    
    def output(self, name, properties):
        if name in self.outputs:
            raise DuplicateOutputException("The output {0} already exists".format(name))

        self.outputs[name] = properties


    def to_dict(self):
        result = {}

        providers = self._to_provider_dict()
        if providers:
            result["provider"] = providers
        if self.variables:
            result["variable"] = self.variables
        if self.data_sources:
            result["data"] = self.data_sources
        if self.resources:
            result["resource"] = self.resources
        if self.outputs:
            result["output"] = self.outputs

        return result


    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


    def _to_provider_dict(self):
        return list(map(lambda p: { p.type: p.properties }, self.providers))


class Variable:
    
    def __init__(self, name):
        self.name = name

    def ref(self):
        return "${{var.{0}}}".format(self.name)


class DuplicateVariableException(RuntimeError):
    pass


class DuplicateOutputException(RuntimeError):
    pass
