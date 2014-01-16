# from devices.SimulatorDevice import SimulatorDevice
# device = SimulatorDevice()

from devices.PhysicalDevice import PhysicalDevice
device = PhysicalDevice()

from apps.PrintSingleTextApp import PrintSingleTextApp
app = PrintSingleTextApp(device)

app.run()
