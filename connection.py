from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result
from websockets import create_connection



# Change to our actual ip
charger_ip = '192.168.1.100'
charger_port = 9000

#initialize websocket connection
ws = create_connection(f"ws://{charger_ip}:{charger_port}")


charge_point = cp(ws)

# change to our actual vendor and model 
response = charge_point.boot_notification('some_vendor', 'some_model')


if isinstance(response, call_result.BootNotification):
    print("BootNotification successful!")
else:
    print("BootNotification failed!")


ws.close()
