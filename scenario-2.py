
'''''SCENARIO'''
'''Today is Spring Daylight savings and the clock will spring forward one hour at 2:00 AM. 
Will there be enough time to charge the fleet to the required SOC by the target time? '''

'''''ANSWER'''
'''Set max rate to be slightly higher? Don't hard code and don't just assume the operator will remember  

Look at how much charge time the fleet has left and determine the charge speed from that time. '''
import asyncio
import datetime

class ElectricVehicle:
    def __init__(self, charge_point, target_time, target_soc, daylight_savings=False):
        self.charge_point = charge_point
        self.target_time = target_time
        self.target_soc = target_soc
        self.daylight_savings = daylight_savings

    async def adjust_charging_rate(self):
        while True:
            # Get the current date and time
            current_date = datetime.datetime.now()

            # Check if daylight savings time is active
            if current_date.month > 3 and current_date.month < 11:
                self.daylight_savings = True
            elif current_date.month == 3 and current_date.weekday() == 6 and current_date.day > 7:
                self.daylight_savings = True
            elif current_date.month == 11 and current_date.weekday() == 6 and current_date.day < 7:
                self.daylight_savings = True
            else:
                self.daylight_savings = False

            if self.daylight_savings:
                # Adjust charging rate for daylight savings scenario
                print("Daylight savings is active. Adjusting charging rate...")
                # Set max charging rate to 90% SOC instead of 80%
                await self.set_charging_profile(90)
            else:
                # Normal charging rate
                print("Daylight savings is not active. Normal charging rate.")
                # Normal charging rate (80% SOC)
                await self.set_charging_profile(80)

            # Sleep for 15 minutes between checks
            await asyncio.sleep(15 * 60)  # Check every 15 minutes

    async def set_charging_profile(self, target_soc):
        # Prepare and send SetChargingProfile OCPP command to adjust charging power
        charging_profile = {
            "chargingProfileId": 1,
            "transactionId": 0,
            "stackLevel": 1,
            "chargingProfilePurpose": "TxDefaultProfile",
            "chargingProfileKind": "Absolute",
            "recurrencyKind": "Daily",
            "chargingSchedule": {
                "duration": 0,
                "startSchedule": datetime.datetime.now().isoformat(),
                "chargingRateUnit": "A",
                "chargingSchedulePeriod": [{
                    "startPeriod": 0,
                    "limit": target_soc * 0.01 * 48  # Charging power in Amperes (48A max limit)
                }]
            }
        }
        response = await self.charge_point.set_charging_profile(charging_profile)
        print("SetChargingProfile response:", response)

class ChargePoint:
    async def set_charging_profile(self, charging_profile):
        # Simulate sending SetChargingProfile command to the charge point
        await asyncio.sleep(1)  # Simulate network delay
        return "Success"

async def main():
    # Create a charge point instance
    charge_point = ChargePoint()

    # Create electric vehicles with different scenarios
    ev1 = ElectricVehicle(charge_point, target_time=3600, target_soc=80)  # Normal scenario
    ev2 = ElectricVehicle(charge_point, target_time=3600, target_soc=90, daylight_savings=True)  # Daylight savings scenario

    # Start adjusting charging rate for each electric vehicle
    asyncio.create_task(ev1.adjust_charging_rate())
    asyncio.create_task(ev2.adjust_charging_rate())

    # Keep the event loop running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
