import brickpi3
import math
import time


class SensorModule:
    def __init__(self, BP, ltouch, rtouch, sonar, sonar_motor, sonar_offset=0):
        self.BP = BP
        self.ltouch = ltouch
        self.rtouch = rtouch
        self.sonar = sonar
        self.sonar_offset = sonar_offset
        self.sonar_motor = sonar_motor

        self.BP.set_sensor_type(ltouch, self.BP.SENSOR_TYPE.TOUCH)
        self.BP.set_sensor_type(rtouch, self.BP.SENSOR_TYPE.TOUCH)
        self.BP.set_sensor_type(sonar, self.BP.SENSOR_TYPE.NXT_ULTRASONIC)

        self.smooth_size = 10
        self.sonar_frames = []

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
        # time.sleep(0.02)
        try:
            dist = self.BP.get_sensor(self.sonar) + self.sonar_offset
            self.sonar_frames.insert(0, dist)
            if len(self.sonar_frames) > self.smooth_size:
                self.sonar_frames.pop()

            return dist

        except brickpi3.SensorError:
            return -1

    def get_sonar_smooth(self):
        self.get_sonar_distance()
        frames = len(self.sonar_frames)
        if (frames > 0):
            return sum(self.sonar_frames) / frames
        else:
            return -1

    def get_sonar_snapshot(self, n=10, warmup=0):
        if warmup > 0:
            self.get_sonar_snapshot(warmup, 0)

        snaps = 0
        acc = 0
        while snaps < n:
            dist = self.get_sonar_distance()
            # print(dist)
            if dist >= 0:
                acc += dist
                snaps += 1

        return acc / n

    def get_sonar_full_rotation(self, interval=1):
