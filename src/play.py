from devices.SimulatorDevice import SimulatorDevice
from apps.CafApp import CafApp

device = SimulatorDevice()
app = CafApp(device)
app.run()
