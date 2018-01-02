class Provider:
    
    def __init__(self, type, properties, resources, data_sources):
        self.type = type
        self.properties = properties
        self.resources = resources
        self.data_sources = data_sources
    
    
    def resource(self, type, name, properties):
        full_type = self._full_type(type)
        self.resources[full_type] = self.resources.get(full_type, {})

        if name in self.resources[full_type]:
            raise DuplicateResourceException("The resource {0}.{1} already exists".format(full_type, name))

        resource = Resource(full_type, name)
        if callable(properties):
            properties = properties(resource)

        if "alias" in self.properties:
            properties = properties.copy()
            properties["provider"] = self.type + "." + self.properties["alias"]

        self.resources[full_type][name] = properties
        return resource


    def data(self, type, name, properties):
        full_type = self._full_type(type)
        self.data_sources[full_type] = self.data_sources.get(full_type, {})

        if name in self.data_sources[full_type]:
            raise DuplicateDataSourceException

        data_source = DataSource(full_type, name)
        if callable(properties):
            properties = properties(data_source)

        self.data_sources[full_type][name] = properties
        return data_source


    def _full_type(self, type):
        return self.type + "_" + type


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


class DuplicateResourceException(RuntimeError):
    pass


class DuplicateDataSourceException(RuntimeError):
    pass
