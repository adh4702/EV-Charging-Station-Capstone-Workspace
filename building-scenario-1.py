# Possible code solution for building scenario 1

from ocpp.v201 import ChargePoint as cp
import asyncio
import pandas as pd
import numpy as np

doc = pd.read_excel('SchmitzData.xlsx', sheet_name = 0)
print(doc)


column_c_values = doc.iloc[3:37971, 2] 

sum_of_values = column_c_values.sum()
average_of_values = column_c_values.mean()

min_value = column_c_values.min()
max_value = column_c_values.max()

print("Average building power consumption (kWh):", average_of_values)
print("Minimum building power consumption(kWh):", min_value)
print("Maximum building power consumption(kWh):", max_value)


'''''''''''''''''''''
Assume these values while we develop our initial implementation:
Max transformer output = 50kWh (artificial constraint for us to work with)
    Buffer amount (to ensure to overages)(20% of max transformer) = 10kWh (buffer incase connected systems/devices 
    get connected during 15-min polling time (i.e. preventing explosion))
    The buffer is because we don't want to reach the transformer's maximum. So we want to pretend
    like we have 10kWh less available

Ideas so far (don't need to worry about this right now, this is for later): 
    buffer should be 2 standard deviations worth of power
    scenario 1 should use 2 sds for determining meter failure


GENERAL CASE logic
Buffer = 10kWh (20% of transformer capacity)
Avg EV consumption during charging = 7.2 kWh (level 2 charger @ 240V, 40A)
Max consumption = 40kWh => 50kWh - 40kWh - buffer = 0kWh available
Avg consumption = 20kWh => 50kWh - 20kWh - buffer = 20kWh available
Min consumption = 8kWh => 50kWh - 8kWh - buffer = 32kWh available

If the expected building power consumption is 25kWh, there is 15kWh available (minus buffer) to power up a charger at 7.2kwH.
Total Building Power - Building Consumption - buffer = EV Power Available

Transformer output > building consumption + ev consumption 
'''''''''''''''''''''

'''
The building energy usage is acting unusual - it is much lower than normal for this time period and does 
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


''' GENERAL CASE pseudocode: increase power usage as building conmsupmtion decreases vice versa'''  

