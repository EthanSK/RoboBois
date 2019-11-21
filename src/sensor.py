import brickpi3
import math
import time
from movement import MovementModule


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

    def get_sonar_full_rotation(self, snap_interval=1, rotate_dps=90, non_snap_rotate_dps=180):
        self.BP.set_motor_limits(
            self.sonar_motor, MovementModule.max_power, MovementModule.max_dps)
        res = []

        def rotate_and_observe(up_to_degress):
            self.BP.set_motor_dps(self.sonar_motor, rotate_dps)
            cur_degrees = self.BP.get_motor_encoder(self.sonar_motor)
            prev_snap_degrees = cur_degrees
            while cur_degrees < up_to_degress: #must be < not <= or too many elems in res
                cur_degrees = self.BP.get_motor_encoder(self.sonar_motor)

                if cur_degrees >= prev_snap_degrees + snap_interval:
                    # take a snapshot
                    dist = self.get_sonar_distance()
                    res.append(dist)
                    prev_snap_degrees = cur_degrees
            self.BP.set_motor_dps(self.sonar_motor, 0)

        # rotate 180 one way, rotate 360 other way, then rotate 180 until reach start
        start_degrees = self.BP.get_motor_encoder(self.sonar_motor)
        rotate_and_observe(start_degrees + 180)

        self.BP.set_motor_dps(self.sonar_motor, -non_snap_rotate_dps)
        cur_degrees = self.BP.get_motor_encoder(self.sonar_motor)
        while cur_degrees >= start_degrees - 180:
            cur_degrees = self.BP.get_motor_encoder(self.sonar_motor)

        rotate_and_observe(start_degrees)

        return res
