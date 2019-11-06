import brickpi3, movement, sensor, vector2

class Robot:
    def __init__(self, movement_module, sensor_module):
        self.movement_module = movement_module
        self.sensor_module = sensor_module
        self.pos = Vector2(0, 0)
        self.rot = 0

    def reset(self):
        self.movement_module.reset()
        self.sensor_module.reset()

    def move_to_pos(self, pos, speed_m = 0.2, turn_speed = 45):
        delta = pos - self.pos
        dist = delta.magnitude()
        angle = delta.angle()

        angle_delta = angle - self.rot
        if abs(angle_delta) < 180:
            self.movement_module.turn(angle_delta, turn_speed)
        else:
            self.movement_module.turn(360 - angle_delta, turn_speed)
        self.rot = angle

        self.movement_module.move_linear(-dist, speed_m)
        self.pos = pos