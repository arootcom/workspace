from ..element import Element, Elements

#
# Container
#

class Container(Element):

    def __init__(self, container, softwareSystemId):
        Element.__init__(self, container)
        self.softwareSystemId = softwareSystemId

    # The name of this container.
    def getName(self):
        if 'name' in self.element.keys():
            return self.element['name']
        return ""

    # A short description of this container.
    def getDescription(self):
        if 'description' in self.element.keys():
            return self.element['description']
        return ""

    # The technology associated with this container (e.g. Apache Tomcat).
    def getTechnology(self):
        if 'technology' in self.element.keys():
            return self.element['technology']
        return ""

    # The URL where more information about this element can be found.
    def getUrl(self):
        if 'url' in self.element.keys():
            return self.element['url']
        return ""

    def getGroup(self):
        if 'group' in self.element.keys():
            return self.element['group']
        return ""

    def getSoftwareSystemId(self):
        return self.softwareSystemId

    def getDict(self):
        elementDict = Element.getDict(self)

        elementDict['name'] = self.getName()
        elementDict['description'] = self.getDescription()
        elementDict['technology'] = self.getTechnology()
        elementDict['url'] = self.getUrl()
        elementDict['group'] = self.getGroup()

        elementDict['softwareSystemId'] = self.softwareSystemId

        return elementDict

#
# Containers
#

class Containers(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return Containers(elements);

