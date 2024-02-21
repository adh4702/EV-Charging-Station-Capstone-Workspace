# Possible code solution for building scenario 1

from ocpp.v201 import ChargePoint as chp
import asyncio
import pandas as pd
import numpy as np


#doc = pd.read_excel('SchmitzData.xlsx', sheet_name = 0)
#print(doc)


'''''''''''''''''''''
Assume these values while we develop our initial implementation:
Max transformer output = 50kWh
    Buffer amount (to ensure to overages) = 10kWh
    The buffer is because we don't want to reach the transformer's maximum. So we want to pretend
    like we have 
Avg EV consumption during charging = 7.2 kWh (per charger, assume 4 chargers)
Max consumption = 40kWh => 50kWh - 40kWh = 10kWh (available)
Avg consumption = 25kWh => 50kWh - 25kWh = 25kWh (available)
Min consumption = 10kWh => 50kWh - 10kWh = 40kWh (available)

If the expected building power consumption is 25kWh, there is 25kWh available to power up 3 chargers at 7.2kwH.
Total Building Power - Building Consumption = EV Power Available

Transformer output > building consumption + ev consumption 
'''''''''''''''''''''

'''
The building energy usage is acting unusual – it is much lower than normal for this time period and does 
not appear to be changing much. Is there a data issue with the meter where it may be frozen or not reporting 
accurate data? What happens if the meter is under reporting the actual usage of the building for a period?

ANSWER
(Meter failure) If power data is reported as 20% below expected power (ex: if total building power consumption is 
normally 25kWh, but it's reported as 16kWh), assume expected power (25kWh -> ideal power consumpation usage) 
Additionally, implement a test to verify connected EVs will be on track to reach expected SOC at the 
scheduled time. Finally, we should have a built in overhead as a safety for all scenarios (buffer). For example, 
if the building has 100MW of power available, we would only use 80MW of that to allow for a buffer. 

point of the buffer is so we dont blow the transformer
everything combined shouldnt be over 50 (building consumption and ev charging)
general case will handle if its above
'''


''' GENERAL CASE: increase power usage as building conmsupmtion decreases vice versa'''  


def check_total_power(building_power, car_charger_power, max_total_power=50):
    total_power = building_power + car_charger_power

    if total_power > max_total_power:
        print(f"Warning: Total power consumption ({total_power} kWh) exceeds the maximum limit ({max_total_power} kWh). Adjust charging schedules.")

    remaining_power = max_total_power - building_power
    if remaining_power < 0:
        remaining_power = 0  # Avoid negative values if the building power already exceeds the limit

    print(f"Remaining available power: {remaining_power} kWh")
# User input section
building_power_consumption = float(input("Enter building power consumption (kWh): "))
car_charger_power_consumption = float(input("Enter car charger power consumption (kWh): "))


check_total_power(building_power_consumption, car_charger_power_consumption)
