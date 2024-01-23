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
parser.add_argument("-view", help="view diagram")
args = parser.parse_args()

file = args.file
if not os.path.isfile(file):
    print(file, " is not file")
    exit()

path = args.path
view = args.view

def ShowNode(node, parent):
    properties = node.getProperties()
    system = properties.getValueByName('System')
    if node.parentId == parent.id:
        infrastructures = node.getLink("infrastructure-nodes", ws)['items']
        tab = "\t\t"
        if int(node.instances) > 1:
            tab = "\t\t\t"
            print("\t\tpackage \"", node.description ,"\" {")
        for instance in range(0, int(node.instances)):
            host = node.name
            host = re.sub(r'\d+..\d+$', f'{instance + 1:02d}', host)
            print(tab +"node node" + node.id + "i" + str(instance), "[")
            print(tab + "\t", host)
            print(tab + "\t---")
            print(tab + "\t", system)
            for infra in infrastructures.getElements():
                properties = infra.getProperties()
                print(tab + "\t-", infra.name + " " + properties.getValueByName("version") if properties.isName("version") else infra.name)
            print(tab + "]")
        if int(node.instances) > 1:
            print("\t\t}")

with open(file, 'r') as raw:
    ws = workspace.Workspace(json.load(raw))
    ds = dispatcher.Dispatcher(ws)
    req = dispatcher.Request("/softwares/" + path)
    res = ds.dispatch(req)

    if res.getType() == "Elements":
        for element in res.getElements().getElements():
            print(element.getDict())
    elif view:
        soft = res.getElement()
        views = soft.getLink('deployment-views', ws)['items']
        view = views.getLink(view, ws)['item']
        nodes = view.getLink("deployment-nodes", ws)['items']
        vms = nodes.getElementsByTag("Virtual Machine")

        print("@startuml\n")
        for center in nodes.getElementsByTag("Data Center").getElements():
            print("node center" + center.id, "as \"", center.name ,"\" {")
            print("\tnode soft as \"", view.getEnvironment(), "/", soft.description, "\" {")
            for vm in vms.getElements():
                ShowNode(vm, center)
                for lxc in nodes.getElementsByTag("Linux Containers").getElements():
                    for lc in nodes.getElementsByTag("Linux Container").getElements():
                        #print(lc.parentId, vm.id)
                        ShowNode(lc, lxc)
            print("\t}")
            print("}")
        print("@enduml\n")
    else:
        soft = res.getElement()
        print("## Комплекс Технических Средств\n")
        print("Подсистема:", soft.group, "\n")
        print("Компонент:", soft.description, "\n")

        views = soft.getLink('deployment-views', ws)['items']
        for view in views.getElements():
            print("###", view.getEnvironment(), "\n")

            print("#### Структурная схема")
            print("![deployment](./" + view.getKey() + ".png)")

            nodes = view.getLink("deployment-nodes", ws)['items']
            print("#### Вычислительные ресурсы\n")
            #print('|----|------------------------------------------|-------|-------|----------------------|')
            print(f'| {"№":2} | {"Хост":40} | {"CPU":5} | {"RAM":5} | {"HDD":20} |')
            print('|----|------------------------------------------|-------|-------|----------------------|')

            virtualMachines = nodes.getElementsByTag("Virtual Machine")
            i = 0
            for virtualMachine in virtualMachines.getElements():
                for instance in range(0, int(virtualMachine.instances)):
                    i = i + 1

                    host = virtualMachine.name
                    host = re.sub(r'\d+..\d+$', f'{instance + 1:02d}', host)

                    properties = virtualMachine.getProperties()
                    cpu = properties.getValueByName('CPU')
                    ram = properties.getValueByName('RAM')
                    hdd = properties.getValueByName('HDD')

                    print(f'| {i:2d} | {host:40} | {cpu:5} | {ram:5} | {hdd:20} |')
            #print('|----|-----------------------------------------|-------|-------|----------------------|')
            print("\n")

            print("#### Сервера\n")
            #print('|----|------------------------------------------|------------------------------------------|-------------------|--------------------------------|--------------------------------|----------------------|')
            print(f'| {"№":2} | {"Наименование":40} | {"Хост":40} | {"IP":17} | {"Порты":30} | {"Сервисы":30} | {"OS":20} |')
            print('|----|------------------------------------------|------------------------------------------|-------------------|--------------------------------|--------------------------------|----------------------|')
            i = 0
            report = re.compile("^(port\d+|port)$")
            virtualMachines = nodes.getElementsByTag("Virtual Machine", "Linux Container")
            for virtualMachine in virtualMachines.getElements():
                for instance in range(0, int(virtualMachine.instances)):
                    i = i + 1
                    host = virtualMachine.name
                    host = re.sub(r'\d+..\d+$', f'{instance + 1:02d}', host)
                    description = virtualMachine.getDescription()
                    properties = virtualMachine.getProperties()
                    system = properties.getValueByName('System')
                    ips = []
                    if properties.isName('IP'):
                        ips = properties.getValueByName('IP')
                        ips = re.sub(r'\s+', '', ips)
                        ips = ips.split(',')
                    ports = []
                    services = []
                    infrastructures = virtualMachine.getLink("infrastructure-nodes", ws)['items']
                    for infra in infrastructures.getElements():
                        properties = infra.getProperties()
                        for name in properties.getNames():
                            if report.search(name):
                                ports.append(properties.getValueByName(name))
                        services.append(infra.name + " " + properties.getValueByName("version") if properties.isName("version") else infra.name)
                    print(f'| {i:2d} | {description:40} | {host:40} | {ips[instance] if ips else "":17} | {ports[0] if ports else "":30} | {services[0] if services else "":30} | {system:20} |')
                    count = len(ports) if len(ports) > len(services) else len(services)
                    for num in range(1, count):
                        print(f'| {"":2} | {"":40} | {"":40} | {"":17} | {ports[num] if num < len(ports) else "":30} | {services[num] if num < len(services) else "":30} | {"":20} |')
            #print('|----|------------------------------------------|------------------------------------------|-------------------|--------------------------------|--------------------------------|----------------------|')
            print("\n")


