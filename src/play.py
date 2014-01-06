from devices.SimulatorDevice import SimulatorDevice
from devices.PhysicalDevice import PhysicalDevice
from apps.CafApp import CafApp
from apps.ToyApp import ToyApp

# device = SimulatorDevice()
device = PhysicalDevice()

# app = CafApp(device)
app = ToyApp(device)

app.run()
