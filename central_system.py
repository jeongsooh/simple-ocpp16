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
from ocpp.v16 import call_result, call

logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):
    @on(Action.Authorize)
    def on_authorize(self, id_tag: str, **kwargs):
        logging.info('========== Got an Authorize Req ==========')
        return call_result.AuthorizePayload(
            id_tag_info={ 'parent_id_tag': id_tag,
                'status': RegistrationStatus.accepted }
        )

    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Boot Notification ==========')
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=240,
            status=RegistrationStatus.accepted
        )

    @on(Action.DiagnosticsStatusNotification)
    def on_diagnostics_status_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Diagnostics Status Notification ==========')
        return call_result.DiagnosticsStatusNotification()

    @on(Action.FirmwareStatusNotification)
    def on_firmware_status_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Firmware Status Notification ==========')
        return call_result.FirmwareStatusNotification()

    @on(Action.Heartbeat)
    def on_heartbeat(self):
        logging.info('========== Got a Heartbeat ==========')
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + "Z"
        )

    @on(Action.MeterValues)
    def on_metervalues(self, connector_id: int, meter_value: str, transaction_id: int):
        logging.info('========== Got a MeterValue Req ==========')
        return call_result.MeterValuesPayload()

    @on(Action.StartTransaction)
    def on_start_transaction(self, connector_id: int, id_tag: str, meter_start: int, timestamp: str, **kwargs):
        logging.info('========== Got a StartTransaction Req ==========')
        return call_result.StartTransactionPayload(
            transaction_id=1,
            id_tag_info={ 'parent_id_tag': id_tag,
                'status': RegistrationStatus.accepted }
        )

    @on(Action.StatusNotification)
    def on_status_notification(self, connector_id: int, error_code: str, status: str, **kwargs):
        logging.info('========== Got a StatusNotification Req ==========')
        return call_result.StatusNotificationPayload()

    @on(Action.StopTransaction)
    def on_stop_transaction(self, id_tag: str, meter_stop: int, timestamp: str, transaction_id: int):
        logging.info('========== Got a StopTransaction Req ==========')
        return call_result.StopTransactionPayload(
            id_tag_info={ 'parent_id_tag': id_tag,
                'status': RegistrationStatus.accepted }
        )

    async def cancel_reservation(self):
        request = call.CancelReservationPayload(
            revervation_id = 1
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Calcel Reservation is accepted.")
            print("===================================")

    async def change_availability(self):
        request = call.ChangeAvailabilityPayload(
            connector_id = 1,
            type = 'AvailabilityType'
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Change Availability is accepted.")
            print("===================================")

    async def change_configuration(self):
        request = call.ChangeConfigurationPayload(
            key = 'str', 
            value = 'Any'
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Change Configuration is accepted.")
            print("===================================")

    async def clear_cache(self):
        request = call.ClearCachePayload()

        response = await self.call(request)
        print("===================================")
        print("Clear Cache transferred.....")
        print("===================================")

    async def clear_charging_profile(self):
        request = call.ClearChargingProfilePayload(
            # options: id, connector_id, charging_profile_purpose, stack_level
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Clear Change Profile is accepted.")
            print("===================================")

    async def get_composite_schedule(self):
        request = call.GetCompositeSchedulePayload(
            connector_id = 1,
            duration = 60
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Get Composite Schedule is accepted.")
            print("===================================")

    async def get_configuration(self):
        request = call.GetConfigurationPayload(
            # options : key
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Get Configuration is accepted.")
            print("===================================")

    async def get_diagnostics(self):
        request = call.GetDiagnosticsPayload(
            location = 'str'
            # options : retries, retry_interval, start_time, stop_time
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Get Diagnostics is accepted.")
            print("===================================")

    async def get_local_list_version(self):
        request = call.GetLocalListVersionPayload()

        response = await self.call(request)
        print("===================================")
        print("Get Local List Version transferred.....")
        print("===================================")

    async def remote_start_transaction(self):
        request = call.RemoteStartTransactionPayload(
            id_tag = 'str'
            # options : connector_id, changing_profile
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Remote Start Transaction is accepted.")
            print("===================================")

    async def remote_stop_transaction(self):
        request = call.RemoteStopTransactionPayload(
            transaction_id = 1
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Remote Stop Transaction is accepted.")
            print("===================================")

    async def reserve_now(self):
        request = call.ReserveNowPayload(
            connector_id = 1,
            expiry_date = "datatime str",
            id_tag = 'str',
            reservation_id = 1, 
            # options: parent_id_tag
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Reserve Now is accepted.")
            print("===================================")

    async def reset(self):
        request = call.ResetPayload(
            type = 'Reset Type'
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Reset is accepted.")
            print("===================================")

    async def send_local_list(self):
        request = call.SendLocalListPayload(
            type = 'Reset Type'
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Send Local List is accepted.")
            print("===================================")

    async def set_charging_profile(self):
        request = call.SetChargingProfilePayload(
            connector_id = 1,
            cs_charging_profiles = 'Dict'
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Set Charging Profile is accepted.")
            print("===================================")

    async def trigger_message(self):
        request = call.TriggerMessagePayload(
            requested_message = 'MessageTrigger'
            # connector_id: Optional[int] = None
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Trigger Message is accepted.")
            print("===================================")

    async def unlock_connector(self):
        request = call.UnlockConnectorPayload(
            connector_id = 1
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Unlock Connector is accepted.")
            print("===================================")

    async def update_firmware(self):
        request = call.UpdateFirmwarePayload(
            location = 'str',
            retrieve_date = 'datetime str'
            # options: retries: int, retry_interval: int
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Update Firmware is accepted.")
            print("===================================")


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
        9001,
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
