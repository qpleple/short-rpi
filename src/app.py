
from devices.SimulatorDevice import SimulatorDevice
device = SimulatorDevice()

# from devices.PhysicalDevice import PhysicalDevice
# device = PhysicalDevice()

from apps.CafApp import CafApp
app = CafApp(device)

# from apps.ToyApp import ToyApp
# app = ToyApp(device)

app.run()
