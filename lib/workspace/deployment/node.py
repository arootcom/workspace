from ..element import Element, Elements

#
# Deploymet Node
#

class DeploymentNode(Element):

    def __init__(self, node, parentId):
        Element.__init__(self, node)
        self.parentId = parentId

    def getName(self):
        if 'name' in self.element.keys():
            return self.element['name']
        return ""

    def getDescription(self):
        if 'description' in self.element.keys():
            return self.element['description']
        return ""

    def getEnvironment(self):
        if 'environment' in self.element.keys():
            return self.element['environment']
        return ""

    def getTechnology(self):
        if 'technology' in self.element.keys():
            return self.element['technology']
        return ""

    def getInstances(self):
        if 'instances' in self.element.keys():
            return self.element['instances']
        return 1

    def getUrl(self):
        if 'url' in self.element.keys():
            return self.element['url']
        return ""

    def getDict(self):
        elementDict = Element.getDict(self)

        elementDict['name'] = self.getName()
        elementDict['description'] = self.getDescription()
        elementDict['environment'] = self.getEnvironment()
        elementDict['technology'] = self.getTechnology()
        elementDict['instances'] = self.getInstances()
        elementDict['url'] = self.getUrl()

        elementDict['parentId'] = self.parentId

        return elementDict

    def getLinks(self):
        return ["infrastructure-nodes"]

    def isLink(self, name):
        for link in self.getLinks():
            if link == name:
                return True
        return False

    def getLink(self, link, ws):
        return {
            "type": "Elements",
            "items": ws.List(link).getElementsByDeploymentNodeId(self.getId())
        }

#
# Deploymet Nodes
#

class DeploymentNodes(Elements):

    def getElementsByTag(self, *tags):
        elements = Elements.getElementsByTag(self, *tags)
        return DeploymentNodes(elements);

    def getElementsByEnvironment(self, environment):
        elements = []
        for container in self.getElements():
            if container.getEnvironment() == environment:
                elements.append(container)
        return DeploymentNodes(elements)

    def isLink(self, name):
        if name in self.elementById.keys():
            return True
        return False

    def getLink(self, link, ws):
        return {
            'type': "Element",
            'item': self.getElementById(link),
        }
