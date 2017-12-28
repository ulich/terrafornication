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
            new_props = properties.copy()
            new_props["provider"] = self.type + "." + self.properties["alias"]
            self.resources[full_type][name] = new_props
        else:
            self.resources[full_type][name] = properties

    def resource_dict(self):
        return self.resources


class DuplicateResourceException(RuntimeError):
    pass
