# domoticz-python-xiaomi-plant-care

Python script for Domoticz that fetches plant data from the Xiaomi Plant Care and presents it to Domoticz.

Create your virtual devices from Setup > Hardware screen

Add a single Dummy hardware device if you haven't already done so

Hit the Create Virtual Sensors button and create the following virtual devices:

- 1 x Temperature
- 1 x Lux
- 1 x Custom Sensor (Axis Label: uS/cm)
- 2 x Percentage
- 1 x Switch

Note down the IDX's for those virtual devices

Make miflora.py executable by chmod +x miflora.py

Open up miflora.py with your preferred file editor

Set the domoticz_ip on line #15 to match your Domoticz IP address (and port if neccesary)

If you have Domoticz login enabled set auth_username and auth_password on line #16 and #17 to match a valid Domoticz user/login.

Set the mac_address on line #18 to the Xiaomi Plant Care Bluetooth LE (BLE) MAC address

Set the individual device ID's for temperature, moisture, light, conductivity, battery and virtual switch
- temperature, switchid on line #59
- moisture, switchid on line #77
- light, switchid on line #95
- conductivity, switchid on line #113
- battery, switchid on line #132
- virtual switch, switchid on line #149

Save changes

Run the file using python3 miflora.py MAC_ADDRESS
(replace MAC_ADDRESS with your BLE MAC address)

That's it :)
