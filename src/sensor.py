import brickpi3
import math
import time
from movement import MovementModule
from particleDataStructures import Canvas
from vector2 import Vector2


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
    
    def get_sonar_rotation_between(self, angle_left, angle_right, snapshot_interval=1, rot_time_del=0.005, should_draw_live=True, start_pos=Vector2(84, 30), draw_rot_offset=0):
        rot_time_del = rot_time_del * snapshot_interval
        self.BP.set_motor_limits(
            self.sonar_motor, MovementModule.max_power, MovementModule.max_dps)
        self.BP.offset_motor_encoder(
            self.sonar_motor, self.BP.get_motor_encoder(self.sonar_motor))  # reset encoder
        res = []
        canvas = Canvas()  # for live drawing
        cur_degrees = 0 #relative to robot

        def rotate_and_observe(up_to_degrees, no_observe=False):
            step = snapshot_interval if cur_degrees < up_to_degrees else -snapshot_interval
            loop = range(cur_degrees + step, up_to_degrees + step, step)
            for new_rot in loop:
                self.BP.set_motor_position(self.sonar_motor, new_rot)
                time.sleep(rot_time_del if not no_observe else rot_time_del / 3)
                if no_observe:
                    continue
                dist = self.get_sonar_distance()
                # -ve so the angle matches with the map angle convention
                new = (-new_rot, dist)
                res.append(new)
                if should_draw_live:

                    self.draw_sonar_line((new[0] + draw_rot_offset, new[1]), canvas, start_pos.x, start_pos.y)
            return up_to_degrees 

        # rotate 180 one way, rotate 360 other way, then rotate 180 until reach start
        cur_degrees = rotate_and_observe(angle_left, True)
        time.sleep(0.3)  # for accuracy
        cur_degrees = rotate_and_observe(angle_right)  # no observing here
        time.sleep(0.3)
        cur_degrees = rotate_and_observe(0, True)
        time.sleep(0.3)

        return res

    def get_sonar_full_rotation(self, snapshot_interval=1, rot_speed=0.005, should_draw_live=True, start_pos=Vector2(84, 30), draw_rot_offset=0):
        rot_speed = rot_speed * snapshot_interval
        self.BP.set_motor_limits(
            self.sonar_motor, MovementModule.max_power, MovementModule.max_dps)
        self.BP.offset_motor_encoder(
            self.sonar_motor, self.BP.get_motor_encoder(self.sonar_motor))  # reset encoder
        res = []
        canvas = Canvas()  # for live drawing
        cur_degrees = 0

        def rotate_and_observe(up_to_degrees, no_observe=False):
            step = snapshot_interval if cur_degrees < up_to_degrees else -snapshot_interval
            loop = range(cur_degrees + step, up_to_degrees + step, step)
            for new_rot in loop:
                self.BP.set_motor_position(self.sonar_motor, new_rot)
                time.sleep(rot_speed if not no_observe else rot_speed / 3)
                if no_observe:
                    continue
                dist = self.get_sonar_distance()
                # -ve so the angle matches with the map angle convention
                new = (-new_rot, dist)
                res.append(new)
                if should_draw_live:

                    self.draw_sonar_line((new[0] + draw_rot_offset, new[1]), canvas, start_pos.x, start_pos.y)
            return up_to_degrees 

        # rotate 180 one way, rotate 360 other way, then rotate 180 until reach start
        cur_degrees = rotate_and_observe(180)
        time.sleep(0.3)  # for accuracy
        cur_degrees = rotate_and_observe(-180, True)  # no observing here
        time.sleep(0.3)
        cur_degrees = rotate_and_observe(0)
        time.sleep(0.3)

        return res

    def draw_sonar_line(self, data, canvas, start_line_x, start_line_y):
        rot_degrees = data[0]
        distance = data[1]
        if distance == -1:
            return
        # we add start because that is essentially the new origin of the graph since we're dealing with distances.
        end_x = start_line_x + distance * math.cos(math.radians(rot_degrees))
        end_y = start_line_y + distance * math.sin(math.radians(rot_degrees))
        canvas.drawLine(
            (start_line_x, start_line_y, end_x, end_y))

    def draw_sonar_full_rotation(self, data):
        # canvas size is bigger since distances can go up to 255
        canvas = Canvas(512)
        start_x = 256
        start_y = start_x
        for el in data:
            self.draw_sonar_line(el, canvas, start_x, start_y)
