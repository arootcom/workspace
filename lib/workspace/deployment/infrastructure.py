from ..element import Element, Elements
from ..relationship import Relationship, Relationships

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

    def getLinks(self):
        return ["relationships"]

    def isLink(self, name):
        for link in self.getLinks():
            if link == name:
                return True
        return False

    def getLink(self, link, ws):
        if link == "relationships":
            relationships = []
            for relationship in self.element['relationships']:
                relationships.append(Relationship(relationship, self.getId()))
            return {
                "type": "Elements",
                "items": Relationships(relationships)
            }

#
# Infrastructure Nodes
#

class InfrastructureNodes(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return InfrastructureNodes(elements);

    def isLink(self, name):
        if name in self.elementById.keys():
            return True
        return False

    def getLink(self, link, ws):
        return {
            'type': "Element",
            'item': self.getElementById(link),
        }

    def getElementsByEnvironment(self, environment):
        elements = []
        for container in self.getElements():
            if container.getEnvironment() == environment:
                elements.append(container)
        return InfrastructureNodes(elements)

    def getElementsByDeploymentNodeId(self, developmentNodeId):
        elements = []
        for container in self.getElements():
            if container.nodeId == developmentNodeId:
                elements.append(container)
        return InfrastructureNodes(elements)
