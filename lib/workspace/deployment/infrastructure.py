from ..element import Element, Elements

#
# Infrastructure Node
#

class InfrastructureNode(Element):

    def __init__(self, infrastructureNode, nodeId):
        Element.__init__(self, infrastructureNode)
        self.nodeId = nodeId

    def getDict(self):
        elementDict = Element.getDict(self)
        elementDict['nodeId'] = self.nodeId
        return elementDict

#
# Infrastructure Nodes
#

class InfrastructureNodes(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return InfrastructureNodes(elements);


