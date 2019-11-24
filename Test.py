from HomieAdapter import HomieAdapter
import sys
import re
import time
import json

ha = HomieAdapter("192.168.178.100","1883","mqtt",False,"rstdelange","pasw0rd")
print("sleeping")
time.sleep(10)


def getdevicesjsonold(ha):
    deviceid, message, parent, device = ha.getdevices()
    results = []
    i=0
    for devicename in device._nodes:
        properties = device._nodes[devicename]._properties
        for prop in properties:
            ha_type = device._nodes[devicename]._type
            if ha_type == "sensor":
                if prop.find("measure") > -1:
                    ha_type = prop[8:]


            results.append(
                {"idx": i, "Name": device._nodes[devicename]._name, "Type": ha_type, "Properties":[{"Name": prop,"Settable": properties[prop]._settable, "Unit": properties[prop]._unit,
                 "Value": properties[prop]._value,"Datatype": properties[prop]._datatype,"Format": properties[prop]._format}]})
            i=i+1
    result = json.dumps({'result': results})
    print(result)
    #print(result[3][4])

def getdevicesjson(ha):
    result = ha.getdevicesjson()
    print(extract_element_from_json(result, ["Devices","Nodes","Topicbase"]))
    print(extract_element_from_json(result, ["Devices","Nodes","Properties","Value"]))


def extract_element_from_json(obj, path):
    '''
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    '''
    def extract(obj, path, ind, arr):
        '''
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        '''
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr

def debug(ha):
    deviceid, message, parent, device=ha.getdevices()

def getdevices(ha):
    deviceid, message, parent, device=ha.getdevices()

    #properties from main device
    print("Main Device properties....")
    print("DEVICE NAME :"+ device._name)
    print("DEVICE HOMIE CONVENTION :"+ device._conventionVersion)
    print("DEVICE STATE :"+ device._state)
    print("DEVICE IP :"+ device._ip)
    print("DEVICE MAC :"+ device._mac)
    print("Node properties....")

    for devicename in device._nodes:

        print(device._nodes[devicename]._name)
        print(devicename)
        print("  ---- "+ device._nodes[devicename]._type)
        properties = device._nodes[devicename]._properties
        for prop in properties:
            print("  -------- "+ prop +" ==value===> " + properties[prop]._value)
            print("  ------------ " + "Settable" + " ==value===> " + properties[prop]._settable)
            print("  ------------ " + "Unit" + " ==value===> " + properties[prop]._unit)
            print("  ------------ " + "Datatype" + " ==value===> " + properties[prop]._datatype)
            print("  ------------ " + "Format" + " ==value===> " + properties[prop]._format)
            print("  ------------ " + "Name" + " ==value===> " + properties[prop]._name)

    #find single value
    print("Print value of livingroom light dim...")
    print(device._nodes["livingroomlight"]._properties["dim"]._value)
    #find properties of node
    print("Print properties of livingroom-thermostat...")
    print(device._nodes["livingroom-thermostat"]._properties)

#getdevicesjson(ha)
getdevices(ha)
#debug(ha)
