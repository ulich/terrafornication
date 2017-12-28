import json
import collections
from provider import Provider

class Terrafornication:

    def __init__(self):
        self.providers = []
        self.resources = {}
    
    def provider(self, type, properties):
        p = Provider(type, properties, self.resources)
        self.providers.append(p)
        return p

    def to_provider_dict(self):
        return map(lambda p: { p.type: p.properties }, self.providers)

    def to_dict(self):
        return {
            "provider": self.to_provider_dict(),
            "resource": self.resources
        }

    def to_json(self):
        return json.dumps(self.to_dict())
