import brickpi3
import movement
import sensor
from vector2 import Vector2
import math


class Robot:
    def __init__(self, movement_module, sensor_module):
        self.movement_module = movement_module
        self.sensor_module = sensor_module
        self.pos = Vector2(0, 0)
        self.rot = 90

    def reset(self):
        self.movement_module.reset()
        self.sensor_module.reset()

    def move_to_pos(self, pos, speed_m=0.2, turn_speed=45):
        if pos != self.pos:
            delta = pos - self.pos
            dist = delta.magnitude()
            angle = delta.angle()

            angle_delta = (self.rot - angle) % 360
            if angle_delta != 0:
                if angle_delta <= 180:
                    self.movement_module.turn(angle_delta, turn_speed)
                else:
                    self.movement_module.turn(angle_delta - 360, turn_speed)
                self.rot = angle

            if dist != 0:
                self.movement_module.move_linear(-dist, speed_m)
                self.pos = pos
