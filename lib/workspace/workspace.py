import re

from .element import Element, Elements
from .deployment.node import DeploymentNode, DeploymentNodes
from .deployment.infrastructure import InfrastructureNode, InfrastructureNodes
from .deployment.container import ContainerInstance, ContainerInstances
from .view import View

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

        self.views = {}
        for view in self.workspace['views']['deploymentViews']:
            self.views[view['key']] = View(view)

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
        return DeploymentNodes(nodes)

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
        for view in self.views.values():
            views.append(view)
        return views

    # View
    def getDeploymentViewByKey(self, key):
        return self.views[key]

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

