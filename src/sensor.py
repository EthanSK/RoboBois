import brickpi3, math

class SensorModule:
    
    def __init__(self, lmotor, rmotor, wh_radius, bd_radius, bias = 0):
        self.BP = brickpi3.BrickPi3()
        BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)


    def set_left_dps(self, dps):
        self.BP.set_motor_limits(self.lmotor, MovementModule.max_power, MovementModule.max_dps)
        self.BP.set_motor_dps(self.lmotor, dps)
