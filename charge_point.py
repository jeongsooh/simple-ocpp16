import asyncio
import logging
from chargepoint import ChargePoint

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)


from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus

logging.basicConfig(level=logging.INFO)


# class ChargePoint(cp):
#     async def send_boot_notification(self):
#         request = call.BootNotificationPayload(
#             charge_point_model="Optimus",
#             charge_point_vendor="The Mobility House"
#         )

#         response = await self.call(request)

#         if response.status == RegistrationStatus.accepted:
#             print("Connected to central system.")


async def main():
    async with websockets.connect(
        'ws://106.10.32.171:9000/CP_1',
        subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(
          cp.start(), 
          cp.send_boot_notification(),
          cp.send_status_notification('Available'),
          cp.send_authorize(),
          cp.send_start_transaction(),
          cp.send_status_notification('Charging'),
          cp.send_meter_value(),
          cp.send_stop_transaction(),
          cp.send_status_notification('Available'),
          cp.send_heartbeat()
        )


if __name__ == '__main__':
    try:
        # asyncio.run() is used when running this example with Python 3.7 and
        # higher.
        asyncio.run(main())
    except AttributeError:
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
