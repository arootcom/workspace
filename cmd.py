import json
import re
import os
import os.path
import sys
import argparse

path = os.path.join(os.path.dirname(__file__), 'lib')
sys.path.append(path)

from workspace import *

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="file workspace.json", required=True)
parser.add_argument("-path", help="path element(s) data")
parser.add_argument("-tag", help="list by tag")
parser.add_argument("--with-tags-cloud", help="tags cloud list", action='store_true')
parser.add_argument("--with-tags", action='store_true')
parser.add_argument("--with-properties", action='store_true')
parser.add_argument("--with-links", action='store_true')
args = parser.parse_args()

file = args.file
if not os.path.isfile(file):
    print(file, " is not file")
    exit()

path = args.path
tag = args.tag
withTagsCloud = args.with_tags_cloud
withTags = args.with_tags
withProperties = args.with_properties
withLinks = args.with_links

def ShowElement(element):
    print(element.getDict())

    if withLinks:
        links = element.getLinks()
        print("\tLinks:")
        for link in element.getLinks():
            print("\t\t/" + path + "/" + link)

    if withTags:
        if not element.isTags():
            print("\tElement with out tags")
        else:
            print("\tTags: ", element.getTags())

    if withProperties:
        if not element.isProperties():
            print ("\tElement with out properties")
        else:
            print("\tProperties:")
            properties = element.getProperties()
            for propertie in properties.getList():
                print("\t\t", propertie)

def ShowElements(elements):
    if withTagsCloud and not elements.isTags():
        print("List with out tags cloud")
        exit(1)
    elif tag and not elements.isTags():
        print("tags not support for this elements")
        exit(1)
    else:
        if withTagsCloud:
            print("Tags Cloud: ", elements.getTagsCloud())
        if tag:
            elements = elements.getElementsByTag(tag)
        for element in elements.getElements():
            ShowElement(element)

with open(file, 'r') as raw:
    ws = workspace.Workspace(json.load(raw))
    if path:
        print("path: /" + path)
        paths = path.split("/")
        if not ws.isKeys(paths[0]):
            print("path not found")
            exit(1)

        elements = ws.List(paths[0])

        if len(paths) == 3:
            key = paths[1]
            element = elements.getElementById(key) if elements.isGetElementById() else elements.getElementByKey(key)
            if not element.isLink(paths[2]):
                print("path not found")
                exit(1)
            data = element.getLink(paths[2], ws)
            if data["type"] == "Element":
                ShowElement(data["item"])
            elif data["type"] == "Dict":
                print(data["item"])
            elif data["type"] == "Elements":
                ShowElements(data["items"])
        elif len(paths) == 2:
            key = paths[1]
            element = elements.getElementById(key) if elements.isGetElementById() else elements.getElementByKey(key)
            ShowElement(element)
        elif len(paths) == 1:
            ShowElements(elements)
        else:
            print("Not found")
    else:
        print("path: /")
        for key in ws.Keys():
            print(key)

