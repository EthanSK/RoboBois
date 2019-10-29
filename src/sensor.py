import brickpi3, math

class SensorModule:
    def __init__(self, ltouch, rtouch, sonar):
        self.BP = brickpi3.BrickPi3()
        self.ltouch = ltouch
        self.rtouch = rtouch
        self.sonar = sonar

        self.BP.set_sensor_type(ltouch, self.BP.SENSOR_TYPE.TOUCH)
        self.BP.set_sensor_type(rtouch, self.BP.SENSOR_TYPE.TOUCH)
        self.BP.set_sensor_type(sonar, self.BP.SENSOR_TYPE.NXT_ULTRASONIC)
    
    def reset(self):
        self.BP.reset_all()

    def get_left_touch(self):
        try:
            return self.BP.get_sensor(self.ltouch)
        except brickpi3.SensorError:
            return False
    
    def get_right_touch(self):
        try:
            return self.BP.get_sensor(self.rtouch)
        except brickpi3.SensorError:
            return False

    def get_sonar_distance(self):
        try:
            return self.BP.get_sensor(self.sonar) / 100
        except brickpi3.SensorError:
            return -1

