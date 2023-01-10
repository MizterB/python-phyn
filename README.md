# python-phyn

A Python library for connecting to the Phyn API

## Example Usage

```python
import pprint

from phyn import Phyn

username = "<Phyn Username>"
password = "<Phyn Password>"

api = Phyn(username, password)
homes = api.homes()
device_id = homes[0].get("device_ids")[0]

# Get device state
device_state = api.devices_state(device_id)
print("DEVICE STATE:")
pprint.pprint(device_state)
print("")

# Get today's hourly water consumption
device_consumption = api.devices_consumption_details(device_id)
print("TODAY'S HOURLY WATER CONSUMPTION:")
pprint.pprint(device_consumption)
print("")

# Get a month's daily water consumption
device_consumption = api.devices_consumption_details(device_id, duration="2023/01")
print("JANUARY 2023 DAILY WATER CONSUMPTION:")
pprint.pprint(device_consumption)
print("")

# Get shutoff valve state
valve_state = api.devices_state(device_id)["sov_status"]["v"]
print(f"VALVE STATE: {valve_state}\n")

# Control the shutoff valve
print("OPENING THE VALVE")
response = api.devices_sov_open(device_id)
pprint.pprint(response)
# print("CLOSING THE VALVE")
# response = api.devices_sov_close(device_id)
# pprint.pprint(response)
```
