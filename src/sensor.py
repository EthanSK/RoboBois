import brickpi3, math

class SensorModule:
    def __init__(self, ltouch, rtouch, sonar):
        self.BP = brickpi3.BrickPi3()
        self.ltouch = ltouch
        self.rtouch = rtouch
        self.sonar = sonar

        BP.set_sensor_type(ltouch, BP.SENSOR_TYPE.TOUCH)
        BP.set_sensor_type(rtouch, BP.SENSOR_TYPE.TOUCH)
        BP.set_sensor_type(sonar, BP.SENSOR_TYPE.SONAR)
    
    def get_left_touch(self):
        return self.BP.get_sensor(ltouch)
    
    def get_right_touch(self):
        return self.BP.get_sensor(rtouch)

