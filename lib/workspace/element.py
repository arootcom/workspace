import re

#
# Element
#

class Element:

    def __init__(self, element):
        self.element = element

    def getId(self):
        return self.element['id']

    def getName(self):
        if 'name' in self.element.keys():
            return self.element['name']
        return ""

    def getEnvironment(self):
        if 'environment' in self.element.keys():
            return self.element['environment']
        return ""

    def getDescription(self):
        if 'description' in self.element.keys():
            return self.element['description']
        return ""

    def getTechnology(self):
        if 'technology' in self.element.keys():
            return self.element['technology']
        return ""

    def getDict(self):
        return {
            'id': self.getId(),
            'name': self.getName(),
            'environment': self.getEnvironment(),
            'description': self.getDescription(),
            'technology': self.getTechnology(),
        }

    def getTags(self):
        tags = []
        for tag in re.split(',', self.element['tags']):
            tag = re.sub(r'^\s+', '', tag)
            tag = re.sub(r'\s+$', '', tag)
            tag = re.sub(r'\s+', ' ', tag)
            tags.append(tag)
        return tags

    def IsTag(self, istag):
        for tag in self.getTags():
            if tag == istag:
                return True
        return False

#
# Elements
#

class Elements:

    def __init__(self, elements):
        self.elements = elements

    def getElements(self):
        return self.elements

    def getElementsByTag(self, tag):
        elements = []
        for container in self.elements:
            if container.IsTag(tag):
                elements.append(container)
        return elements

    def getTagsCloud(self):
        tags = {}
        for element in self.elements:
            for tag in element.getTags():
                if not tag in tags.keys():
                    tags[tag] = 1
        return list(tags.keys())

    def count(self):
        return len(self.elements)
