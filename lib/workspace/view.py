from .properties import Properties

#
# View
#

class View:

    def __init__(self, element):
        self.element = element

    def getKey(self):
        return self.element['key']

    def isProperties(self):
        if 'properties' in self.element.keys():
            return True
        return False

    def getProperties(self):
        return Properties(self.element['properties'])

    def isTags(self):
        return False

#
# Views
#

class Views:

    def __init__(self, elements):
        self.elements = elements
        self.elementByKey = {}
        for element in self.elements:
            self.elementByKey[element.getKey()] = element

    def getElementByKey(self, key):
        return self.elementByKey[key]


    def getElements(self):
        return self.elements

