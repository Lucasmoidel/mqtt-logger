import json
import time
from paho.mqtt import client as mqtt


def logNode(payload):
    f = open("NodeList.json", "r")
    data = json.load(f)
    f.close()
    nodes = data["nodes"]
    exists = False
    for i in range(len(nodes)):
        if nodes[i]["id"] == payload["id"]:
            exists = True
            nodes[i]["sName"] = payload["shortname"]
            nodes[i]["lName"] = payload["longname"]
            print("update " +  nodes[i]["lName"])
    if not exists:
        new = {"id": payload["id"], "sName": payload["shortname"], "lName": payload["longname"]}
        #print(new)
        nodes.append(new)


    f = open("NodeList.json", "w")
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()

def logTel(payload):
    f = open("NodeList.json", "r")
    data = json.load(f)
    f.close()
    nodes = data["nodes"]
    exists = False
    nodeI = -1
    for i in range(len(nodes)):
        if nodes[i]["id"] == f"!{payload["from"]:08x}" :
            nodeI = i
        #print(i)

    if(nodeI == -1):
        new = {"id": f"!{payload["from"]:08x}"}
        nodes.append(new)
        nodeI = len(nodes)-1
    node = nodes[nodeI]
    if "telemetry" not in node:
        node["telemetry"] = []
    new = {}
    new["time"] = payload["timestamp"]
    if "temperature" in payload:
        new["temperature"] = payload["temperature"]

    if "relative_humidity" in payload:
        new["relative_humidity"] = payload["relative_humidity"]

    if "barometric_pressure" in payload:
        new["barometric_pressure"] = payload["barometric_pressure"]

    if "gas_resistance" in payload:
        new["gas_resistance"] = payload["gas_resistance"]

    if "voltage" in payload:
        new["voltage"] = payload["voltage"]

    if "current" in payload:
        new["current"] = payload["current"]

    if "voltage_ch1" in payload:
        new["voltage_ch1"] = payload["voltage_ch1"]

    if "current_ch1" in payload:
        new["current_ch1"] = payload["current_ch1"]

    if "voltage_ch2" in payload:
        new["voltage_ch2"] = payload["voltage_ch2"]

    if "current_ch2" in payload:
        new["current_ch2"] = payload["current_ch2"]

    if "voltage_ch3" in payload:
        new["voltage_ch3"] = payload["voltage_ch3"]

    if "current_ch3" in payload:
        new["current_ch3"] = payload["current_ch3"]

    node["telemetry"].append({"time": 5})

    f = open("NodeList.json", "w")
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()

def func(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    payload = json.loads(payload)
    if payload["type"] == "nodeinfo":
        logNode(payload["payload"])
    elif payload["type"] == "telemetry":
        logTel(payload)




# Setup: Connect to public broker and publish topic
client = mqtt.Client()
client.connect("dad-dell-proxmox", 1883)
client.on_message = func

client.subscribe("/mesh/2/json/MediumFast/!433ce1d4")
client.loop_forever()