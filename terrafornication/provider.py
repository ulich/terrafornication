class Provider:
    
    def __init__(self, type, properties, resources):
        self.type = type
        self.properties = properties
        self.resources = resources
    
    def resource(self, type, name, properties):
        full_type = self.type + "_" + type
        self.resources[full_type] = self.resources.get(full_type, {})

        if name in self.resources[full_type]:
            raise DuplicateResourceException("The resource {}.{} already exists".format(full_type, name))

        if "alias" in self.properties:
            properties = properties.copy()
            properties["provider"] = self.type + "." + self.properties["alias"]

        self.resources[full_type][name] = properties
        return Resource(full_type, name, properties)

    def resource_dict(self):
        return self.resources


class Resource:
    
    def __init__(self, type, name, properties):
        self.type = type
        self.name = name
        self.properties = properties

    def ref(self, property):
        return "${{{}.{}.{}}}".format(self.type, self.name, property)


class DuplicateResourceException(RuntimeError):
    pass
