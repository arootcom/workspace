#
# Properties
#

class Properties:
    def __init__(self, properties):
        self.properties = properties

    def getValueByName(self, name):
        return self.properties[name]

    def getNames(self):
        names = []
        for name in self.properties:
            names.append(name)
        return names

    def getList(self):
        properties = []
        for name in self.properties:
            properties.append({
                'name': name,
                'value': self.properties[name],
            })
        return properties

