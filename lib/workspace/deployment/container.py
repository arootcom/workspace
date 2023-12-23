from ..element import Element, Elements

#
# Container Instance
#

class ContainerInstance(Element):

    def __init__(self, containerInstance, nodeId):
        Element.__init__(self, containerInstance)
        self.nodeId = nodeId

    def getContainerId(self):
        return self.element['containerId']

    def getDict(self):
        return {
            'id': self.getId(),
            'description': self.getDescription(),
            'nodeId': self.nodeId,
        }

#
# Container Instances
#

class ContainerInstances(Elements):

    def getContainerInstancesByContainerId(self, containerId):
        containers = []
        for container in self.elements:
            if container.getContainerId() == containerId:
                containers.append(container)
        return ContainerInstances(containers)

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return ContainerInstances(elements);

