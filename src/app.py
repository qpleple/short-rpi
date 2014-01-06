from devices.SimulatorDevice import SimulatorDevice
from apps.CafApp import CafApp

device = SimulatorDevice()
# device = PhysicalDevice()

app = CafApp(device)
# app = ToyApp(device)

app.run()
