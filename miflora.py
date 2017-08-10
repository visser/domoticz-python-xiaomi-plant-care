#!/usr/bin/python

from miflora.miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY

import datetime
import base64
import json
import urllib
import urllib.request
from urllib.parse import quote
from requests.auth import HTTPBasicAuth
import base64

domoticz_ip = ""
auth_username = ""
auth_password = ""
mac_address = ""

poller = MiFloraPoller(mac_address)

temperature = poller.parameter_value("temperature")
moisture = poller.parameter_value(MI_MOISTURE)
light = poller.parameter_value(MI_LIGHT)
battery = poller.parameter_value(MI_BATTERY)
conductivity = poller.parameter_value(MI_CONDUCTIVITY)

print("Getting data from Mi Flora")
print("FW: {}".format(poller.firmware_version()))
print("Name: {}".format(poller.name()))
print("Temperature: {}".format(temperature))
print("Moisture: {}".format(moisture))
print("Light: {}".format(light))
print("Conductivity: {}".format(conductivity))
print("Battery: {}".format(battery))

def log(message):
  print(message)

def domoticzrequest (url):
  
  global auth_username
  global auth_password
  base64string = base64.b64encode( bytes(auth_username + ":" + auth_password, 'utf-8') )
  
  headers = {"Authorization": "Basic %s" % quote(base64string)}
  req = urllib.request.Request(url, None, headers)
  response = urllib.request.urlopen(req)
  output = response.read()
  return output

temperature = str(temperature)
moisture = str(moisture)
light = str(light)
conductivity = str(conductivity)
battery = str(battery)

# Temperature
switchid = ""
domoticzurl = "http://" + domoticz_ip + "/json.htm?type=devices&rid=" + switchid
device="temperature"
json_object = domoticzrequest(domoticzurl).decode('utf8')
json_object = json.loads(json_object)
if json_object["status"] == "OK":
  if json_object["result"][0]["idx"] == switchid:
    existing_temperature = json_object["result"][0]["Data"]
    print( "Existing temperature: " + existing_temperature)
    existing_temperature.replace(" C","")

if temperature == existing_temperature:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + temperature + ", status unchanged")
else:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + temperature + ", status updated")
  domoticzrequest("http://" + domoticz_ip + "/json.htm?type=command&param=udevice&idx=" + switchid + "&nvalue=0&svalue=" + temperature)

# Moisture
switchid = ""
domoticzurl = "http://" + domoticz_ip + "/json.htm?type=devices&rid=" + switchid
device="general"
json_object = domoticzrequest(domoticzurl).decode('utf8')
json_object = json.loads(json_object)
if json_object["status"] == "OK":
  if json_object["result"][0]["idx"] == switchid:
    existing_moisture = json_object["result"][0]["Data"]
    print( "Existing moisture: " + existing_moisture)
    existing_moisture.replace(".00%","")

if moisture == existing_moisture:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + moisture + ", status unchanged")
else:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + moisture + ", status updated")
  domoticzrequest("http://" + domoticz_ip + "/json.htm?type=command&param=udevice&idx=" + switchid + "&nvalue=0&svalue=" + moisture)

# Light
switchid = ""
domoticzurl = "http://" + domoticz_ip + "/json.htm?type=devices&rid=" + switchid
device="lux"
json_object = domoticzrequest(domoticzurl).decode('utf8')
json_object = json.loads(json_object)
if json_object["status"] == "OK":
  if json_object["result"][0]["idx"] == switchid:
    existing_light = json_object["result"][0]["Data"]
    print( "Existing light: " + existing_light)
    existing_light.replace(" Lux","")

if light == existing_light:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + light + ", status unchanged")
else:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + light + ", status updated")
  domoticzrequest("http://" + domoticz_ip + "/json.htm?type=command&param=udevice&idx=" + switchid + "&nvalue=0&svalue=" + light)

# Conductivity
switchid = ""
domoticzurl = "http://" + domoticz_ip + "/json.htm?type=devices&rid=" + switchid
device="custom_sensor"
json_object = domoticzrequest(domoticzurl).decode('utf8')
json_object = json.loads(json_object)
if json_object["status"] == "OK":
  if json_object["result"][0]["idx"] == switchid:
    existing_conductivity = json_object["result"][0]["Data"]
    print( "Existing conductivity: " + existing_conductivity)
    existing_conductivity.replace(" uS/cm","")
    existing_conductivity.replace(" meow","")

if conductivity == existing_conductivity:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + conductivity + ", status unchanged")
else:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + conductivity + ", status updated")
  domoticzrequest("http://" + domoticz_ip + "/json.htm?type=command&param=udevice&idx=" + switchid + "&nvalue=0&svalue=" + conductivity)

# Battery
switchid = ""
domoticzurl = "http://" + domoticz_ip + "/json.htm?type=devices&rid=" + switchid
device="percentage"
json_object = domoticzrequest(domoticzurl).decode('utf8')
json_object = json.loads(json_object)
if json_object["status"] == "OK":
  if json_object["result"][0]["idx"] == switchid:
    existing_battery = json_object["result"][0]["Data"]
    existing_battery.replace(" .00%","")

if battery == existing_battery:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + battery + ", status unchanged")
else:
  log (datetime.datetime.now().strftime("%H:%M:%S") + "- " + device + ": " + battery + ", status updated")
  domoticzrequest("http://" + domoticz_ip + "/json.htm?type=command&param=udevice&idx=" + switchid + "&nvalue=0&svalue=" + battery)

# Reset Plant switch
switchid = ""
domoticzurl = "http://" + domoticz_ip + "/json.htm?type=command&param=switchlight&idx=" + switchid + "&switchcmd=Off"
domoticzrequest(domoticzurl)

# Notify Domoticz logging
domoticzurl = 'http://' + domoticz_ip + '/json.htm?type=command&param=addlogmessage&message=plant-logging-from-Raspberry-Pi'
domoticzrequest(domoticzurl)

# Done!
