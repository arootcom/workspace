import re

from .properties import Properties

#
# Element
#

class Element:

    def __init__(self, element):
        self.element = element

    def getId(self):
        return self.element['id']

    def getDict(self):
        return {
            'id': self.getId()
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

    def getProperties(self):
        return Properties(self.element['properties'])

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
