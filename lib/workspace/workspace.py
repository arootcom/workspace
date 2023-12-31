import re

from .system.software import Software, Softwares
from .system.container import Container, Containers
from .deployment.node import DeploymentNode, DeploymentNodes
from .deployment.infrastructure import InfrastructureNode, InfrastructureNodes
from .deployment.container import ContainerInstance, ContainerInstances
from .deployment.view import DeploymentView, DeploymentViews

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
            deploymentViews.append(DeploymentView(deploymentView))

        self.items = {
            'softwares': Softwares(softwares),
            'containers': Containers(containers),
            'deployment-views': DeploymentViews(deploymentViews),
            'deployment-nodes': DeploymentNodes(nodes),
            'container-instances': ContainerInstances(containerInstances),
            'infrastructure-nodes': InfrastructureNodes(infrastructureNodes),
        }

    def List(self, cmd):
        if cmd in self.items.keys():
            return self.items[cmd]

    def Keys(self):
        return self.items.keys()

    def isKeys(self, key):
        if key in self.items.keys():
            return True
        return False

