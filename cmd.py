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
parser.add_argument("-key", help="deployment view key")
parser.add_argument("-list", help="list relations entity", choices=['containers', 'deployment-nodes', 'container-instances', 'infrastructure-nodes'])
parser.add_argument("-tag", help="list by tag")
parser.add_argument("--tags-cloud", help="tags cloud list", action='store_true')
parser.add_argument("--with-tags", action='store_true')
parser.add_argument("--with-properties", action='store_true')
parser.add_argument("--check", action='store_true')
args = parser.parse_args()

file = args.file
if not os.path.isfile(file):
    print(file, " is not file")
    exit()

key = args.key
ls = args.list
tag = args.tag
is_tags_cloud = args.tags_cloud
withTags = args.with_tags
is_check = args.check
withProperties = args.with_properties

with open(file, 'r') as raw:
    ws = workspace.Workspace(json.load(raw))

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
            if is_tags_cloud:
                print("Tags Cloud: ", listElements[ls].getTagsCloud())
            if tag:
                elements = elements.getElementsByTag(tag)
            print(ls, ":")
            for element in elements.getElements():
                if ls == 'containers' and is_check:
                    containerInstances = listElements['container-instances'].getContainerInstancesByContainerId(element.getId())
                    if containerInstances.count() == 0:
                        print("\t", element.getDict())
                        print("\t\tcontainer instances count:", containerInstances.count())
                    continue

                print("\t", element.getDict())
                if withTags:
                    print("\t\tTags: ", element.getTags())
                if withProperties:
                    print("\t\tProperties:")
                    properties = element.getProperties()
                    for propertie in properties.getList():
                        print("\t\t\t", propertie)
    else:
        print("DeploymentView:")
        for view in ws.getDeploymentViews():
            print(view.getDict())
