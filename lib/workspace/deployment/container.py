from ..element import Element, Elements

#
# Container Instance
#

class ContainerInstance(Element):

    def __init__(self, containerInstance, nodeId):
        Element.__init__(self, containerInstance)
        self.nodeId = nodeId

    # The ID of the container this is an instance of
    def getContainerId(self):
        return self.element['containerId']

    # The number/index of this instance
    def getInstanceId(self):
        return self.element['instanceId']

    # The deployment environment in which this container instance resides (e.g. "Development", "Live", etc)
    def getEnvironment(self):
        if 'environment' in self.element.keys():
            return self.element['environment']
        return ""

    def getDict(self):
        elementDict = Element.getDict(self)

        elementDict['containerId'] = self.getContainerId()
        elementDict['instanceId'] = self.getInstanceId()
        elementDict['environment'] = self.getEnvironment()

        elementDict['nodeId'] = self.nodeId

        return elementDict

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

