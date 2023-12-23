#
# View
#
class View:

    def __init__(self, view):
        self.view = view

    def getSoftwareSystemId(self):
        return self.view['softwareSystemId']

    def getEnvironment(self):
        return self.view['environment']

    def getDict(self):
        return {
            'softwareSystemId': self.view['softwareSystemId'],
            'environment': self.view['environment'],
            'key': self.view['key'],
        }

