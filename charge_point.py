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

from ocpp.routing import on
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus, Action

logging.basicConfig(level=logging.INFO)

heartbeat_interval = 60

async def heartbeat_send(cp, interval):
    while True:
        print(interval)
        await cp.send_heartbeat()
        await asyncio.sleep(interval)

async def main():


    async with websockets.connect(
        'ws://127.0.0.1:9001/webServices/ocpp/100013',
        subprotocols=['ocpp1.6']
    ) as ws:

    # async with websockets.connect(
    #     'ws://emcms.watchpoint.co.kr/webServices/ocpp/100198',
    #     subprotocols=['ocpp1.6']
    # ) as ws:

        cp = ChargePoint('100013', ws)

        await asyncio.gather(
          cp.start(), 
          cp.send_boot_notification(),
          heartbeat_send(cp, heartbeat_interval)
        )

        # await asyncio.gather(
        #   cp.start(), 
        #   cp.send_boot_notification(),
        #   cp.send_status_notification('Available'),
        #   cp.send_authorize(),
        #   cp.send_start_transaction(),
        #   cp.send_status_notification('Charging'),
        #   cp.send_meter_value(),
        #   cp.send_stop_transaction(),
        #   cp.send_status_notification('Available'),
        #   cp.send_heartbeat()
        # )


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


# [
#     2,
#     "1007",
#     "MeterValue",
#     {
#         "connectorId":1,
#         "meterValue":[
#             {
#                 "sampledValue":[
#                     {"context":"Sample_Periodic","format":"Raw","unit":"Wh","value":"600"}, 
#                     {"context":"Sample_Periodic","format":"Raw","unit":"Wh","value":"600"}
#                 ],
#                 "timestamp":"2022-06-07T16:55:14Z"
#             }
#         ],
#         "transactionId":1
#     }
# ]

# [
#     2,
#     "58627f71-3742-4434-8977-2f49e94b00a7",
#     "MeterValues",
#     {
#         "connectorId":1,
#         "meterValue":[
#             {
#                 "timestamp":"2022-06-08T01:50:49.907787",
#                 "sampledValue":[
#                     {"value":"20","context":"Sample.Periodic","format":"Raw","unit":"Wh"}
#                 ]
#             },
#             {
#                 "timestamp":"2022-06-08T01:50:49.907787",
#                 "sampledValue":[{"value":"20","context":"Sample.Periodic","format":"Raw","unit":"Wh"}]
#             },
#             {"timestamp":"2022-06-08T01:50:49.907787","sampledValue":[{"value":"30","context":"Sample.Periodic","format":"Raw","unit":"Wh"}]},
#             {"timestamp":"2022-06-08T01:50:49.907787","sampledValue":[{"value":"30","context":"Sample.Periodic","format":"Raw","unit":"Wh"}]}
#         ],
#         "transactionId":2
#     }
# ]