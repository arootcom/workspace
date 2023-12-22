import re

from .element import Element, Elements

class Workspace:

    def __initNodes__(self, deploymentNodes, parentId):
        for node in deploymentNodes:
            self.nodes[node['id']] = DeploymentNode(node, parentId)

            containerInstances = []
            if 'containerInstances' in node.keys():
                for containerInstance in node['containerInstances']:
                    self.containerInstances[containerInstance['id']] = ContainerInstance(containerInstance, node['id'])

            infrastructureNodes = []
            if 'infrastructureNodes' in node.keys():
                for infrastructureNode in node['infrastructureNodes']:
                    self.infrastructureNodes[infrastructureNode['id']] = InfrastructureNode(infrastructureNode, node['id'])

            if 'children' in node.keys():
                self.__initNodes__(node['children'], node['id'])

    def __init__(self, workspace):
        self.workspace = workspace

        self.nodes = {}
        self.containerInstances = {}
        self.infrastructureNodes = {}
        self.__initNodes__(self.workspace['model']['deploymentNodes'], None)

        self.containers = {}
        for softwareSystem in self.workspace['model']['softwareSystems']:
            if 'containers' in softwareSystem.keys():
                for data in softwareSystem['containers']:
                    container = Container(data, softwareSystem['id'])
                    self.containers[container.getId()] = container

    # Container Instances
    def getContainerInstancesByEnviroment(self, environment):
        containerInstances = []
        for containerInstance in self.containerInstances.values():
            if containerInstance.getEnvironment() == environment:
                containerInstances.append(containerInstance)
        return ContainerInstances(containerInstances)

    # Deploymet Nodes
    def getDeploymentNodesByEnvironment(self, environment):
        nodes = []
        for node in self.nodes.values():
            if node.getEnvironment() == environment:
                nodes.append(node)
        return DelpoymentNodes(nodes)

    # Infrastructure Nodes
    def getInfrastructureNodesByEnviroment(self, environment):
        infrastructureNodes = []
        for infrastructureNode in self.infrastructureNodes.values():
            if infrastructureNode.getEnvironment() == environment:
                infrastructureNodes.append(infrastructureNode)
        return InfrastructureNodes(infrastructureNodes)

    # Deployment Views
    def getDeploymentViews(self):
        views = []
        for view in self.workspace['views']['deploymentViews']:
            views.append({
                'softwareSystemId': view['softwareSystemId'],
                'environment': view['environment'],
                'key': view['key'],
            })
        return views

    def getDeploymentViewByKey(self, key):
        for view in self.workspace['views']['deploymentViews']:
            if key == view['key']:
                return {
                    'softwareSystemId': view['softwareSystemId'],
                    'environment': view['environment'],
                    'key': view['key'],
                }

    # Software
    def getSoftwareSystemById(self, id):
        for system in self.workspace['model']['softwareSystems']:
            if id == system['id']:
                return {
                    'id': system['id'],
                    'group': system['group'],
                    'name': system['name'],
                }

    # Software Containers
    def geContainersBySoftwareSystemId(self, id):
        containers = []
        for container in self.containers.values():
            if container.getSoftwareSystemId() == id:
                containers.append(container)
        return Containers(containers)

#
# Properties
#
class Properties:
    def __init__(self, properties):
        self.properties = properties

    def getValueByName(self, name):
        return self.properties[name]

    def getNames(self):
        names = []
        for name in self.properties:
            names.append(name)
        return names

    def getList(self):
        properties = []
        for name in self.properties:
            properties.append({
                'name': name,
                'value': self.properties[name],
            })
        return properties

#
# Deploymet Nodes
#

class DelpoymentNodes(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return DelpoymentNodes(elements);

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

    def getProperties(self):
        return Properties(self.element['properties'])

#
# Infrastructure Nodes
#

class InfrastructureNodes(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return InfrastructureNodes(elements);

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

    def getProperties(self):
        return Properties(self.element['properties'])

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

    def getProperties(self):
        return Properties(self.element['properties'])

#
# Containers
#

class Containers(Elements):

    def getElementsByTag(self, tag):
        elements = Elements.getElementsByTag(self, tag)
        return Containers(elements);

#
# Container
#

class Container(Element):

    def __init__(self, container, softwareSystemId):
        Element.__init__(self, container)
        self.softwareSystemId = softwareSystemId

    def getSoftwareSystemId(self):
        return self.softwareSystemId

    def getDict(self):
        elementDict = Element.getDict(self)
        elementDict['softwareSystemId'] = self.softwareSystemId
        return elementDict

    def getProperties(self):
        return Properties(self.element['properties'])

