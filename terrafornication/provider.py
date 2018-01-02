class Provider:
    
    def __init__(self, type, properties, tf):
        self.type = type
        self.properties = properties
        self.tf = tf
    
    
    def resource(self, type, name, properties):
        if "alias" in self.properties:
            properties = properties.copy()
            properties["provider"] = self.type + "." + self.properties["alias"]
        
        return self.tf.resource(self._full_type(type), name, properties)
    

    def data(self, type, name, properties):
        return self.tf.data(self._full_type(type), name, properties)


    def _full_type(self, type):
        return self.type + "_" + type
