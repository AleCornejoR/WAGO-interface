# LIBRERIES
from pymodbus.client.sync import ModbusTcpClient


# MODEL CLASS DEFINITION
# source.model.py
class Model:
    def __init__(self):
        pass


# WAGO CLASS DEFINITION
class WagoPLC:

    def __init__(self, ip, coils, actLow, virtual):
        self.ip = ip
        self.modbus = None
        self.virtual = virtual

        self.coils = [actLow] * coils
        self.numcoils = coils
        self.tester_index = 1

        self.VALVE_OPEN = not actLow
        self.VALVE_CLOSED = actLow
        print("ok WAGO")

    def connection(self):
        client = ModbusTcpClient(self.ip)
        print("ok connection")

        if not self.virtual:
            connected = client.connect()
        else:
            connected = True

        if not connected:
            print(
                f"Could not connect to WAGO at IP {self.ip}! Double-check IP address and connections."
            )
            self.connection_status = "FAIL"
            return

        self.modbus = client
        self.connection_status = "SUCCESS"

    def resetValves(self):
        for i in range(self.numcoils):
            self.setValve(i, self.VALVE_CLOSED)

    def resetValvesN(self):
        for i in range(self.numcoils):
            self.setValve(i, self.VALVE_OPEN)

    def setValve(self, coil, value):
        if self.modbus == None:
            print("WAGO not connected!")
            return

        if not self.virtual:
            self.modbus.write_coil(coil, value)
        else:
            print(
                f"VIRT coil set {coil} to {'open' if value == self.VALVE_OPEN else 'closed'}"
            )
        self.coils[coil] = value

    def isValveOpen(self, coil):
        return self.coils[coil] == self.VALVE_OPEN

    def toggleValve(self, coil):
        self.setValve(coil, not self.coils[coil])
