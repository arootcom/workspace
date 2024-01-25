from .element import Element, Elements

#
# Relationship
#

class Relationship(Element):

    def __init__(self, relationship, elementId):
        Element.__init__(self, relationship)
        self.elementId = elementId

    # A short description of this relationship.
    def  getDescription(self):
        if 'description' in self.element.keys():
            return self.element['description']
        return ""

    # The URL where more information about this relationship can be found.
    def getUrl(self):
        if 'url' in self.element.keys():
            return self.element['url']
        return ""

    # The ID of the source element.
    def getSourceId(self):
        return self.element['sourceId']

    # The ID of the destination element.
    def getDestinationId(self):
        return self.element['destinationId']

    # The technology associated with this relationship (e.g. HTTPS, JDBC, etc)
    def getTechnology(self):
        if 'technology' in self.element.keys():
            return self.element['technology']
        return ""

    #
    def getDict(self):
        elementDict = Element.getDict(self)

        elementDict['description'] = self.getDescription()
        elementDict['url'] = self.getUrl()
        elementDict['sourceId'] = self.getSourceId()
        elementDict['destinationId'] = self.getDestinationId()
        elementDict['technology'] = self.getTechnology()

        elementDict['elementId'] = self.elementId

        return elementDict

#
# Relationships
#

class Relationships(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return Relationships(elements);
