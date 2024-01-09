from ..view import View, Views

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
        return ["software", "environment", "container-instances", "deployment-nodes", "infrastructure-nodes", "containers"]

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

