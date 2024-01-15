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

    # The workspace ID.
    def getId(self):
        return self.workspace['id']

    # The name of the workspace.
    def getName(self):
        return self.workspace['name']

    # A short description of the workspace.
    def getDescription(self):
        return self.workspace['description']

    # A version number for the workspace.
    def getVersion(self):
        if 'version' in self.workspace.keys():
            return self.workspace['version']
        return ""

    # The last modified date, in ISO 8601 format (e.g. "2018-09-08T12:40:03Z").
    def getLastModifiedDate(self):
        return self.workspace['lastModifiedDate']

    # A string identifying the user who last modified the workspace (e.g. an e-mail address or username).
    def getLastModifiedUser(self):
        if 'lastModifiedUser' in self.workspace.keys():
            return self.workspace['lastModifiedUser']
        return ""

    # A string identifying the agent that was last used to modify the workspace (e.g. "structurizr-java/1.2.0").
    def getLastModifiedAgent(self):
        if 'lastModifiedAgent' in self.workspace.keys():
            return self.workspace['lastModifiedAgent']
        return ""

    #
    def getDict(self):
        return {
            'id': self.getId(),
            'name': self.getName(),
            'description': self.getDescription(),
            'version': self.getVersion(),
            'lastModifiedDate': self.getLastModifiedDate(),
            'lastModifiedUser': self.getLastModifiedUser(),
            'lastModifiedAgent': self.getLastModifiedAgent(),
        }

    #
    def isTags(self):
        return False

    #
    def isProperties(self):
        return False

    #
    def List(self, cmd):
        if cmd in self.items.keys():
            return self.items[cmd]

    #
    def getLink(self, link, ws):
        return {
            "type": "Elements",
            "items": ws.List(link)
        }

    #
    def getLinks(self):
        return self.items.keys()

    #
    def isLink(self, key):
        if key in self.items.keys():
            return True
        return False

