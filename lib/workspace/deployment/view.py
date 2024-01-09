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

#
# Deploymet Nodes
#

class DeploymentViews(Views):

    def isTags(self):
        return False

