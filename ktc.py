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
args = parser.parse_args()

file = args.file
if not os.path.isfile(file):
    print(file, " is not file")
    exit()

path = args.path

with open(file, 'r') as raw:
    ws = workspace.Workspace(json.load(raw))
    ds = dispatcher.Dispatcher(ws)
    req = dispatcher.Request("/softwares/" + path)
    res = ds.dispatch(req)

    if res.getType() == "Elements":
        for element in res.getElements().getElements():
            print(element.getDict())
    else:
        soft = res.getElement()
        print("## Комплекс Технических Средств\n")
        print("Подсистема:", soft.group)
        print("Компонент:", soft.description, "\n")

        views = soft.getLink('deployment-views', ws)['items']
        for view in views.getElements():
            print("###", view.getEnvironment(), "\n")

            nodes = view.getLink("deployment-nodes", ws)['items']
            print("#### Вычислительные ресурсы\n")
            print('+----+------------------------------------------+-------+-------+----------------------+')
            print(f'| {"№":2} | {"Хост":40} | {"CPU":5} | {"RAM":5} | {"HDD":20} |')
            print('+----+------------------------------------------+-------+-------+----------------------+')

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
            print('+----+-----------------------------------------+-------+-------+----------------------+')
            print("\n")

            print("#### Сервера\n")
            print('+----+------------------------------------------+------------------------------------------+-------------------+--------------------------------+--------------------------------+----------------------+')
            print(f'| {"№":2} | {"Наименование":40} | {"Хост":40} | {"IP":17} | {"Порты":30} | {"Сервисы":30} | {"OS":20} |')
            print('+----+------------------------------------------+------------------------------------------+-------------------+--------------------------------+--------------------------------+----------------------+')
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
                    ports = []
                    services = []
                    infrastructures = virtualMachine.getLink("infrastructure-nodes", ws)['items']
                    for infra in infrastructures.getElements():
                        properties = infra.getProperties()
                        for name in properties.getNames():
                            if report.search(name):
                                ports.append(properties.getValueByName(name))
                        services.append(infra.name + " " + properties.getValueByName("version") if properties.isName("version") else infra.name)
                    print(f'| {i:2d} | {description:40} | {host:40} | {" ":17} | {ports[0] if ports else "":30} | {services[0] if services else "":30} | {system:20} |')
                    count = len(ports) if len(ports) > len(services) else len(services)
                    for num in range(1, count):
                        print(f'| {"":2} | {"":40} | {"":40} | {"":17} | {ports[num] if num < len(ports) else "":30} | {services[num] if num < len(services) else "":30} | {"":20} |')
            print('+----+------------------------------------------+------------------------------------------+-------------------+--------------------------------+--------------------------------+----------------------+')
            print("\n")


