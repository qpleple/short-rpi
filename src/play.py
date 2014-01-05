from devices.SimulatorDevice import SimulatorDevice
from apps.ToyApp import ToyApp

device = SimulatorDevice()
app = ToyApp(device)
app.run()
