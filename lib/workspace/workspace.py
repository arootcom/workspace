import re

from .system.software import Software, Softwares
from .system.container import Container, Containers
from .deployment.node import DeploymentNode, DeploymentNodes
from .deployment.infrastructure import InfrastructureNode, InfrastructureNodes
from .deployment.container import ContainerInstance, ContainerInstances
from .view import View, Views

class Workspace:

    def __initNodes__(self, nodes, containerInstances, infrastructureNodes, deploymentNodes, parentId):
        for node in deploymentNodes:
            nodes.append(DeploymentNode(node, parentId))
            if 'containerInstances' in node.keys():
                for containerInstance in node['containerInstances']:
                    containerInstances.append(ContainerInstance(containerInstance, node['id']))
            if 'infrastructureNodes' in node.keys():
                for infrastructureNode in node['infrastructureNodes']:
                    infrastructureNodes.append(InfrastructureNode(infrastructureNode, node['id']))
            if 'children' in node.keys():
                self.__initNodes__(nodes, containerInstances, infrastructureNodes, node['children'], node['id'])

    def __init__(self, workspace):
        self.workspace = workspace

        nodes = []
        containerInstances = []
        infrastructureNodes = []
        self.__initNodes__(nodes, containerInstances, infrastructureNodes, self.workspace['model']['deploymentNodes'], None)

        softwares = []
        containers = []
        for softwareSystem in self.workspace['model']['softwareSystems']:
            softwares.append(Software(softwareSystem))
            if 'containers' in softwareSystem.keys():
                for data in softwareSystem['containers']:
                    containers.append(Container(data, softwareSystem['id']))

        deploymentViews = []
        for deploymentView in self.workspace['views']['deploymentViews']:
            deploymentViews.append(View(deploymentView))

        self.items = {
            'softwares': Softwares(softwares),
            'containers': Containers(containers),
            'deployment-views': Views(deploymentViews),
            'deployment-nodes': DeploymentNodes(nodes),
            'container-instances': ContainerInstances(containerInstances),
            'infrastructure-nodes': InfrastructureNodes(infrastructureNodes),
        }

    def List(self, cmd):
        if cmd in self.items.keys():
            return self.items[cmd]

    def ElementByKey(self, ls, key):
        if self.items[ls].isGetElementById():
            return self.items[ls].getElementById(key)
        else:
            return self.items[ls].getElementByKey(key)

    def Keys(self):
        return self.items.keys()

    def isKeys(self, key):
        if key in self.items.keys():
            return True
        return False

'''
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

    # Software Containers
    def geContainersBySoftwareSystemId(self, id):
        containers = []
        for container in self.containers.values():
            if container.getSoftwareSystemId() == id:
                containers.append(container)
        return Containers(containers)
'''
