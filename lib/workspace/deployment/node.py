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

#
# Deploymet Nodes
#

class DeploymentNodes(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return DeploymentNodes(elements);

    def getElementsByEnvironment(self, environment):
        elements = []
        for container in self.getElements():
            if container.getEnvironment() == environment:
                elements.append(container)
        return DeploymentNodes(elements)
