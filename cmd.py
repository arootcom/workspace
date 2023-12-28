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
parser.add_argument("-list", help="list relations entity")
parser.add_argument("-key", help="deployment view key")
parser.add_argument("-tag", help="list by tag")
parser.add_argument("--with-tags-cloud", help="tags cloud list", action='store_true')
parser.add_argument("--with-tags", action='store_true')
parser.add_argument("--with-properties", action='store_true')
#parser.add_argument("--check", action='store_true')
args = parser.parse_args()

file = args.file
if not os.path.isfile(file):
    print(file, " is not file")
    exit()

key = args.key
ls = args.list
tag = args.tag
withTagsCloud = args.with_tags_cloud
withTags = args.with_tags
#is_check = args.check
withProperties = args.with_properties

def ShowElement(element):
    print(element.getDict())
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

with open(file, 'r') as raw:
    ws = workspace.Workspace(json.load(raw))
    if ls:
        if not ws.isKeys(ls):
            print("list not found")
            exit(1)
        if key:
            print("/" + ls + "/" + key)
            element = ws.ElementByKey(ls, key)
            ShowElement(element)
        else:
            elements = ws.List(ls)
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
    else:
        for key in ws.Keys():
            print(key)

'''
    if key:
        print("Key: ", key)
        view = ws.getDeploymentViewByKey(key)
        print("DeploymentView: ", view.getDict())

        system = ws.getSoftwareSystemById(view.getSoftwareSystemId())
        print("SoftwareSystem: ", system.getDict())

        reLs = re.compile(r"^(containers|deployment-nodes|container-instances|infrastructure-nodes)$")
        listElements = {
            'containers': ws.geContainersBySoftwareSystemId(system.getId()),
            'deployment-nodes': ws.getDeploymentNodesByEnvironment(view.getEnvironment()),
            'container-instances': ws.getContainerInstancesByEnviroment(view.getEnvironment()),
            'infrastructure-nodes': ws.getInfrastructureNodesByEnviroment(view.getEnvironment()),
        }

        if ls and re.fullmatch(reLs, ls):
            elements = listElements[ls]
            print(ls, ":")
            for element in elements.getElements():
                if ls == 'containers' and is_check:
                    containerInstances = listElements['container-instances'].getContainerInstancesByContainerId(element.getId())
                    if containerInstances.count() == 0:
                        print("\t", element.getDict())
                        print("\t\tcontainer instances count:", containerInstances.count())
                    continue

'''
