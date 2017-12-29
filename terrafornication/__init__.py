import json
import collections
from provider import Provider

class Terrafornication:

    def __init__(self):
        self.providers = []
        self.resources = {}
        self.data_sources = {}
    

    def provider(self, type, properties):
        p = Provider(type, properties, self.resources, self.data_sources)
        self.providers.append(p)
        return p


    def to_dict(self):
        return {
            "provider": self._to_provider_dict(),
            "data": self.data_sources,
            "resource": self.resources
        }


    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)


    def _to_provider_dict(self):
        return map(lambda p: { p.type: p.properties }, self.providers)
