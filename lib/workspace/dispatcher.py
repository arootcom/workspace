import re

#
class Dispatcher:

    def __init__(self, workspace):
        self.workspace = workspace

    def dispatch(self, req):
        i = 0
        element = self.workspace
        data = {
            'type': "Element",
            'item': self.workspace,
        }

        for part in req.getParts():
            i = i + 1
            if not element.isLink(part):
                data = {
                    'type': "Error",
                    'note': "Not found",
                }
                break

            data = element.getLink(part, self.workspace)
            if data["type"] == "Element" and i != req.getLenParts():
                element = data["item"]
            elif data["type"] == "Elements" and i != req.getLenParts():
                element = data["items"]

        return Response(data)

#
class Request:

    def __init__(self, path):
        self.path = path
        path = re.sub(r'/+', '/', path)
        path = re.sub(r'^/', '', path)
        path = re.sub(r'/$', '', path)
        self.parts = path.split("/") if path else []

    def getPath(self):
        return self.path

    def getParts(self):
        return self.parts

    def getLenParts(self):
        len(self.parts)

#
class Response:

    def __init__(self, data):
        self.data = data

    def getType(self):
        return self.data['type']

    def getElement(self):
        return self.data['item']

    def getElements(self):
        return self.data['items']

    def getNote(self):
        return self.data['note']


