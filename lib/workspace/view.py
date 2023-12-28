from .properties import Properties

#
# View
#

class View:

    def __init__(self, element):
        self.element = element

    def getKey(self):
        return self.element['key']

    def getSoftwareSystemId(self):
        return self.element['softwareSystemId']

    def getEnvironment(self):
        return self.element['environment']

    def isProperties(self):
        if 'properties' in self.element.keys():
            return True
        return False

    def getProperties(self):
        return Properties(self.element['properties'])

    def isTags(self):
        return False

    def getDict(self):
        return {
            'softwareSystemId': self.element['softwareSystemId'],
            'environment': self.element['environment'],
            'key': self.getKey(),
        }

#
# Views
#

class Views:

    def __init__(self, elements):
        self.elements = elements
        self.elementByKey = {}
        for element in self.elements:
            self.elementByKey[element.getKey()] = element

    def isGetElementById(self):
        return False

    def getElementByKey(self, key):
        return self.elementByKey[key]


    def getElements(self):
        return self.elements

    def isTags(self):
        return False
