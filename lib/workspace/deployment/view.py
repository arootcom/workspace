from ..view import View, Views
from ..system.container import Containers

#
# Deployment View
#

class DeploymentView(View):

    def getEnvironment(self):
        return self.element['environment']

    def getSoftwareSystemId(self):
        return self.element['softwareSystemId']

    def getDict(self):
        return {
            'softwareSystemId': self.element['softwareSystemId'],
            'environment': self.element['environment'],
            'key': self.getKey(),
        }

    def getLinks(self):
        return [
            "software", "environment",
            "container-instances", "deployment-nodes", "infrastructure-nodes",
            "containers",
            "containers-wo-instances",
        ]

    def isLink(self, name):
        for link in self.getLinks():
            if link == name:
                return True
        return False

    def getLink(self, link, ws):
        if link == "software":
            return {
                "type": "Element",
                "item": ws.List("softwares").getElementById(self.getSoftwareSystemId())
            }
        elif link == "environment":
            return {
                "type": "Dict",
                "item": {
                    'environment': self.getEnvironment(),
                },
            }
        elif link == "containers":
            return {
                "type": "Elements",
                "items": ws.List(link).getElementsBySoftwareSystemId(self.getSoftwareSystemId())
            }
        elif link == "containers-wo-instances":
            items = []
            containers = ws.List("containers").getElementsBySoftwareSystemId(self.getSoftwareSystemId())
            instances = ws.List("container-instances").getElementsByEnvironment(self.getEnvironment())
            for container in containers.getElements():
                append = True
                for instance in instances.getElements():
                    if instance.getContainerId() == container.getId():
                        append = False
                        break
                if append:
                    items.append(container)

            return {
                "type": "Elements",
                "items": Containers(items)
            }
        else:
            return {
                "type": "Elements",
                "items": ws.List(link).getElementsByEnvironment(self.getEnvironment())
            }


#
# Deploymet Nodes
#

class DeploymentViews(Views):

    def isTags(self):
        return False

    def isLink(self, name):
        if name in self.elementByKey.keys():
            return True
        return False

    def getLink(self, link, ws):
        return {
            'type': "Element",
            'item': self.getElementByKey(link),
        }

    def getElementsBySoftwareSystemId(self, softwareSystemId):
        elements = []
        for container in self.getElements():
            if container.getSoftwareSystemId() == softwareSystemId:
                elements.append(container)
        return DeploymentViews(elements)
