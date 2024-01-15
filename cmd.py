import json
import re
import os
import os.path
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib') )

from workspace import *

parser = argparse.ArgumentParser()
parser.add_argument("-file", help="file workspace.json", required=True)
parser.add_argument("-path", help="path element(s) data", default="")
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
    print("Element:")
    print("\tAttributes:")
    data = element.getDict()
    for key in data.keys():
        print("\t\t" + key, ":", data[key])

    if withLinks:
        links = element.getLinks()
        print("\tLinks:")
        for link in element.getLinks():
            print("\t\t" + link)

    if withTags:
        print("\tTags:")
        if not element.isTags():
            print("\t\tElement with out tags")
        else:
            print("\t\t", element.getTags())

    if withProperties:
        print("\tProperties:")
        if not element.isProperties():
            print ("\t\tElement with out properties")
        else:
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
    ds = dispatcher.Dispatcher(ws)
    req = dispatcher.Request(path)
    print("Path: ", req.getPath())

    res = ds.dispatch(req)
    if res.getType() == "Element":
        ShowElement(res.getElement())
    elif res.getType() == "Elements":
        ShowElements(res.getElements())
    elif res.getType() == "Error":
        print(res.getNote())

