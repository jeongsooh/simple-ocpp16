from datetime import datetime
from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus

class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus",
            charge_point_vendor="The Mobility House"
        )

        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            print("===================================")
            print("Connected to central system.")
            print("===================================")

    async def send_heartbeat(self):
        request = call.HeartbeatPayload()

        response = await self.call(request)
        print("===================================")
        print("Heartbeat transferred.....")
        print("===================================")


    async def send_authorize(self):
        request = call.AuthorizePayload(
            id_tag = "1010010112345678"
        )

        response = await self.call(request)
        if response.id_tag_info['status'] == RegistrationStatus.accepted:
            print("===================================")
            print("Auth.req is accepted.")
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

    async def send_status_notification(self, cpstatus):
        request = call.StatusNotificationPayload(
            connector_id=1,
            error_code='NoError',
            status=cpstatus
        )

        response = await self.call(request)
        print("===================================")
        print("StatusNotification transferred.....")
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