import flash
import json
import requests
import ssl


#
# testConnection
#
def testConnection(ip):

    try:
        response = requests.get("http://" + ip + "/api/test/config")

        js = json.loads(response.content)
        if (js["name"] == "Philips hue"):
            return True;

    except Exception as e:
        return False;


#
# createUser
#
def createUser(ip):

    try:
        response = requests.post("http://" + ip + "/api", json={"devicetype": "my_hue_app#Riverdi IoT Display"})

        js = json.loads(response.content)
        return js[0]["success"]["username"];

    except Exception as e:
        return None;


#
# turnLight
#
def turnLight(ip,user,num,state):

    try:
        addr = "http://" + ip + "/api/" + user + "/lights/" + num + "/state"
        requests.put(addr, json={"on":state})
    except Exception as e:
        return None;


#
# changeColor
#
def changeColor(ip,user,num,state, sat, bri, hue):

    try:
        addr = "http://" + ip + "/api/" + user + "/lights/" + num + "/state"
        requests.put(addr, json={"on":state, "sat":sat, "bri":bri, "hue":hue})
    except Exception as e:
        return None;
