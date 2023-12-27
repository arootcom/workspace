import re

from .element import Element, Elements
from .system.software import Software
from .system.container import Container, Containers
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

        self.softwares = {}
        self.containers = {}
        for softwareSystem in self.workspace['model']['softwareSystems']:
            self.softwares[softwareSystem['id']] = Software(softwareSystem)
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
        return self.softwares[id]

    # Software Containers
    def geContainersBySoftwareSystemId(self, id):
        containers = []
        for container in self.containers.values():
            if container.getSoftwareSystemId() == id:
                containers.append(container)
        return Containers(containers)

