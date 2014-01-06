from devices.SimulatorDevice import SimulatorDevice
from devices.PhysicalDevice import PhysicalDevice
from apps.ToyApp import ToyApp
from apps.CafApp import CafApp

# device = SimulatorDevice()
device = PhysicalDevice()

app = CafApp(device)
# app = ToyApp(device)

app.run()
