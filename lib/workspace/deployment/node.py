from ..element import Element, Elements

#
# Deploymet Node
#

class DeploymentNode(Element):

    def __init__(self, node, parentId):
        Element.__init__(self, node)
        self.parentId = parentId

    def getDict(self):
        elementDict = Element.getDict(self)
        elementDict['parentId'] = self.parentId
        return elementDict

#
# Deploymet Nodes
#

class DeploymentNodes(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return DeploymentNodes(elements);
