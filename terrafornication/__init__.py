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
        p = provider.Provider(type, properties, self)
        self.providers.append(p)
        return p


    def resource(self, type, name, properties):
        self.resources[type] = self.resources.get(type, {})

        if name in self.resources[type]:
            raise DuplicateResourceException("The resource {0}.{1} already exists".format(type, name))

        resource = Resource(type, name)
        if callable(properties):
            properties = properties(resource)

        self.resources[type][name] = properties
        return resource


    def data(self, type, name, properties):
        self.data_sources[type] = self.data_sources.get(type, {})

        if name in self.data_sources[type]:
            raise DuplicateDataSourceException

        data_source = DataSource(type, name)
        if callable(properties):
            properties = properties(data_source)

        self.data_sources[type][name] = properties
        return data_source

    
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


class Resource:
    
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def ref(self, property):
        return "${{{0}.{1}.{2}}}".format(self.type, self.name, property)


class DataSource:
    
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def ref(self, property):
        return "${{data.{0}.{1}.{2}}}".format(self.type, self.name, property)


class DuplicateVariableException(RuntimeError):
    pass

class DuplicateResourceException(RuntimeError):
    pass

class DuplicateDataSourceException(RuntimeError):
    pass

class DuplicateOutputException(RuntimeError):
    pass
