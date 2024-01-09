from ..element import Element, Elements

#
# Infrastructure Node
#

class InfrastructureNode(Element):

    def __init__(self, infrastructureNode, nodeId):
        Element.__init__(self, infrastructureNode)
        self.nodeId = nodeId

    # The name of this infrastructure node
    def getName(self):
        if 'name' in self.element.keys():
            return self.element['name']
        return ""

    # A short description of this infrastructure node
    def getDescription(self):
        if 'description' in self.element.keys():
            return self.element['description']
        return ""

    # The technology associated with this infrastructure node (e.g. "Route 53").
    def getTechnology(self):
        if 'technology' in self.element.keys():
            return self.element['technology']
        return ""

    # The deployment environment in which this infrastructure node resides (e.g. "Development", "Live", etc).
    def getEnvironment(self):
        if 'environment' in self.element.keys():
            return self.element['environment']
        return ""

    # The URL where more information about this element can be found.
    def getUrl(self):
        if 'url' in self.element.keys():
            return self.element['url']
        return ""

    #
    def getDict(self):
        elementDict = Element.getDict(self)

        elementDict['name'] = self.getName()
        elementDict['description'] = self.getDescription()
        elementDict['technology'] = self.getTechnology()
        elementDict['environment'] = self.getEnvironment()
        elementDict['url'] = self.getUrl()

        elementDict['nodeId'] = self.nodeId

        return elementDict

#
# Infrastructure Nodes
#

class InfrastructureNodes(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return InfrastructureNodes(elements);


    def getElementsByEnvironment(self, environment):
        elements = []
        for container in self.getElements():
            if container.getEnvironment() == environment:
                elements.append(container)
        return InfrastructureNodes(elements)

