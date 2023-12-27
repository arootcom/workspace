from ..element import Element, Elements

#
# Software System
#

class Software(Element) :

    def __init__(self, software):
        Element.__init__(self, software)

    # The name of this software syste
    def getName(self):
        if 'name' in self.element.keys():
            return self.element['name']
        return ""

    # A short description of this software system.
    def getDescription(self):
        if 'description' in self.element.keys():
            return self.element['description']
        return ""

    # The location of this software system.
    # enum: - External, - Internal, - Unspecifie
    def getLocation(self):
        if 'location' in self.element.keys():
            return self.element['location']
        return ""

    #  The URL where more information about this element can be found
    def getUrl(self):
        if 'url' in self.element.keys():
            return self.element['url']
        return ""

    # The name of the group in which this software system should be included in.
    def getGroup(self):
        if 'group' in self.element.keys():
            return self.element['group']
        return ""

    def getDict(self):
        elementDict = Element.getDict(self)

        elementDict['name'] = self.getName()
        elementDict['description'] = self.getDescription()
        elementDict['location'] = self.getLocation()
        elementDict['url'] = self.getUrl()
        elementDict['group'] = self.getGroup()


        return elementDict

#
# Software Systems
#


