from datetime import datetime
import time
from ocpp.routing import on
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus

class ChargePoint(cp):
    heartbeat_interval = 60
    async def send_authorize(self):
        request = call.AuthorizePayload(
            id_tag = "1010010112345678"
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Auth.req is accepted.")
            print("===================================")

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus",
            charge_point_vendor="The Mobility House"
        )

        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            heartbeat_interval = response.interval
            print("===================================")
            print("Connected to central system.")
            print(response)
            print("===================================")

    async def send_data_transfer(self):
        request = call.DataTransferPayload(
            vendor_id="gresystem",
            message_id="DataTransferMessageId",
            data="user defined data"
        )

        response = await self.call(request)
        if response.status == "Accepted":
            print("===================================")
            print("Data Transfer to central system: Accepted")
            print("===================================")

    async def send_diagnostics_status_notification(self):
        request = call.DiagnosticsStatusNotificationPayload(
            status = "diagnostics status"
        )

        response = await self.call(request)
        # if response.status == "Accepted":
        print("===================================")
        print("Diagnostics Status Notification to central system")
        print("===================================")

    async def send_firmware_status_notification(self):
        request = call.FirmwareStatusNotificationPayload(
            status = "Firmware status"
        )

        response = await self.call(request)
        # if response.status == "Accepted":
        print("===================================")
        print("Firmware Status Notification to central system")
        print("===================================")

    async def send_heartbeat(self):
        request = call.HeartbeatPayload()

        response = await self.call(request)
        print("===================================")
        print("Heartbeat transferred.....")
        print("===================================")

    async def send_meter_value(self):
        cur_time = datetime.now().isoformat()
        request = call.MeterValuesPayload(
            connector_id=1,
            transaction_id=2,
            meter_value=[
                {"timestamp":cur_time,"sampledValue":[{"value":"20","context":"Sample.Periodic","format":"Raw","unit":"Wh"}]},
                {"timestamp":cur_time,"sampledValue":[{"value":"20","context":"Sample.Periodic","format":"Raw","unit":"Wh"}]},
                {"timestamp":cur_time,"sampledValue":[{"value":"30","context":"Sample.Periodic","format":"Raw","unit":"Wh"}]},
                {"timestamp":cur_time,"sampledValue":[{"value":"30","context":"Sample.Periodic","format":"Raw","unit":"Wh"}]}
            ]
        )

        response = await self.call(request)
        print("===================================")
        print("MeterValue transferred.....")
        print("===================================")

    async def send_start_transaction(self):
        request = call.StartTransactionPayload(
            connector_id=1,
            id_tag='1010010112345678',
            meter_start=212,
            timestamp=datetime.now().isoformat()
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("StartTransaction started. transaction_id: ", response.transaction_id)
            print("===================================")

    async def send_stop_transaction(self):
        request = call.StopTransactionPayload(
            id_tag='1010010112345678',
            meter_stop=250,
            timestamp=datetime.now().isoformat(),
            transaction_id=3,
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("StopTransaction started. transaction_id: ")
            print("===================================")

    async def send_status_notification(self, cpstatus):
        request = call.StatusNotificationPayload(
            connector_id=1,
            error_code='NoError',
            status='Available'
        )

        response = await self.call(request)
        print("===================================")
        print("StatusNotification transferred.....")
        print("===================================")

    @on(Action.CancelReservation)
    def on_cancel_reservation(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Boot Notification ==========')
        return call_result.CancelReservationPayload(
            status = 'CancelReservationStatus'
        )

    @on(Action.ChangeAvailability)
    def on_change_availability(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Change Availability ==========')
        return call_result.ChangeAvailabilityPayload(
            status = 'AvailabilityStatus'
        )

    @on(Action.ChangeConfiguration)
    def on_change_configuration(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Change Configuration ==========')
        return call_result.ChangeConfigurationPayload(
            status = 'ConfigurationStatus'
        )

    @on(Action.ChangeConfiguration)
    def on_change_configuration(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Change Configuration ==========')
        return call_result.ChangeConfigurationPayload(
            status = 'ConfigurationStatus'
        )

    @on(Action.ClearCache)
    def on_clear_cache(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Clear Cache ==========')
        return call_result.ClearCachePayload(
            status = 'ClearCacheStatus'
        )

    @on(Action.ClearChargingProfile)
    def on_clear_charging_profile(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Clear Charging Profile ==========')
        return call_result.ClearChargingProfilePayload(
            status = 'ClearChargingProfileStatus'
        )

    @on(Action.GetCompositeSchedule)
    def on_get_composite_schedule(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Get Composite Schedule ==========')
        return call_result.GetCompositeSchedulePayload(
            status = 'GetCompositeScheduleStatus'
            # options: connector_id: int, schedule_start: str, charging_schedule: Dict
        )

    @on(Action.GetConfiguration)
    def on_get_configuration(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Get Configuration ==========')
        return call_result.GetConfigurationPayload(
            # options: configuration_key: List, unknown_key: List
        )

    @on(Action.GetDiagnostics)
    def on_get_diagnostics(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Get Diagnostics ==========')
        return call_result.GetDiagnosticsPayload(
            # options: file_name: str
        )

    @on(Action.GetLocalListVersion)
    def on_get_local_list_version(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Get Local List Version ==========')
        return call_result.GetLocalListVersionPayload(
            list_version = 1
        )

    @on(Action.RemoteStartTransaction)
    def on_remote_start_transaction(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Remote Start Transaction ==========')
        return call_result.RemoteStartTransactionPayload(
            status = 'RemoteStartStopStatus'
        )

    @on(Action.RemoteStopTransaction)
    def on_remote_stop_transaction(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Remote Stop Transaction ==========')
        return call_result.RemoteStopTransactionPayload(
            status = 'RemoteStartStopStatus'
        )

    @on(Action.ReserveNow)
    def on_reserve_now(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Reserve Now ==========')
        return call_result.ReserveNowPayload(
            status = 'ReservationStatus'
        )

    @on(Action.Reset)
    def on_reset(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Reset ==========')
        return call_result.ResetPayload(
            status = 'ResetStatus'
        )

    @on(Action.SendLocalList)
    def on_send_local_list(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Send Local List ==========')
        return call_result.SendLocalListPayload(
            status = 'UpdateStatus'
        )

    @on(Action.SetChargingProfile)
    def on_set_charging_profile(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Set Charging Profile ==========')
        return call_result.SetChargingProfilePayload(
            status = 'ChargingProfileStatus'
        )

    @on(Action.TriggerMessage)
    def on_trigger_message(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Trigger Message ==========')
        return call_result.TriggerMessagePayload(
            status = 'TriggerMessageStatus'
        )

    @on(Action.UnlockConnector)
    def on_unlock_connector(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Unlock Connector ==========')
        return call_result.UnlockConnectorPayload(
            status = 'UnlockStatus'
        )

    @on(Action.UpdateFirmware)
    def on_update_firmware(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        logging.info('========== Got a Update Firmware ==========')
        return call_result.UpdateFirmwarePayload(
            # pass
        )




