import brickpi3, movement, sensor

class Robot:
    def __init__(self, movement_module, sensor_module):
        self.movement_module = movement_module
        self.sensor_module = sensor_module

    def reset(self):
        self.movement_module.reset()
        self.sensor_module.reset()