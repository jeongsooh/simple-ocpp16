import asyncio
import logging
from datetime import datetime

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
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Boot Notification ==========')
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=240,
            status=RegistrationStatus.accepted
        )

    @on(Action.Heartbeat)
    def on_heartbeat(self):
        logging.info('========== Got a Heartbeat ==========')
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"
        )

    @on(Action.Authorize)
    def on_authorize(self, id_tag: str, **kwargs):
        logging.info('========== Got an Authorize Req ==========')
        return call_result.AuthorizePayload(
            id_tag_info={ 'parent_id_tag': id_tag,
                'status': RegistrationStatus.accepted }
        )

    @on(Action.StatusNotification)
    def on_status_notification(self, connector_id: int, error_code: str, status: str, **kwargs):
        logging.info('========== Got a StatusNotification Req ==========')
        return call_result.StatusNotificationPayload(
        )

    @on(Action.StartTransaction)
    def on_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, **kwargs):
        logging.info('========== Got a StartTransaction Req ==========')
        return call_result.StartTransactionPayload(
            transaction_id=1,
            id_tag_info={ 'parent_id_tag': id_tag,
                'status': RegistrationStatus.accepted }
        )

    @on(Action.MeterValues)
    def on_metervalues(self, connector_id: int, meter_value: str, transaction_id: int):
        logging.info('========== Got a MeterValue Req ==========')
        return call_result.MeterValuesPayload(
        )

    @on(Action.StopTransaction)
    def on_stop_transaction(self, id_tag: str, meter_stop: int, timestamp: str, transaction_id: int):
        logging.info('========== Got a StopTransaction Req ==========')
        return call_result.StopTransactionPayload(
            id_tag_info={ 'parent_id_tag': id_tag,
                'status': RegistrationStatus.accepted }
        )






async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    try:
        requested_protocols = websocket.request_headers[
            'Sec-WebSocket-Protocol']
    except KeyError:
        logging.info("Client hasn't requested any Subprotocol. "
                     "Closing Connection")
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning('Protocols Mismatched | Expected Subprotocols: %s,'
                        ' but client supports  %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols)
        return await websocket.close()

    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    logging.info('==============================')

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )

    logging.info("Server Started listening to new connections...")
    await server.wait_closed()


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
