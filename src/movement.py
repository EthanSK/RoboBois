import brickpi3
import math


class MovementModule:
    max_power = 50
    max_dps = 0

    def __init__(self, BP, lmotor, rmotor, wh_radius, bd_radius, bias=0):
        self.BP = BP
        self.lmotor = lmotor
        self.rmotor = rmotor

        self.wh_radius = wh_radius
        self.wh_circ = wh_radius * 2 * math.pi

        self.bd_radius = bd_radius
        self.bd_circ = bd_radius * 2 * math.pi

        self.bias = bias

        self.ldps = 0
        self.rdps = 0

    def set_left_dps(self, dps):
        self.BP.set_motor_limits(
            self.lmotor, MovementModule.max_power, MovementModule.max_dps)
        self.BP.set_motor_dps(self.lmotor, dps)
        self.ldps = dps

    def set_right_dps(self, dps):
        self.BP.set_motor_limits(
            self.rmotor, MovementModule.max_power, MovementModule.max_dps)
        self.BP.set_motor_dps(self.rmotor, dps * (1 + self.bias))
        self.rdps = dps

    def get_left_rot(self):
        return self.BP.get_motor_encoder(self.lmotor)

    def get_right_rot(self):
        return self.BP.get_motor_encoder(self.rmotor)

    def float_all(self):
        self.BP.set_motor_power(self.lmotor, self.BP.MOTOR_FLOAT)
        self.BP.set_motor_power(self.rmotor, self.BP.MOTOR_FLOAT)

    def get_linear_dps(self, speed_ms):
        rps = speed_ms / self.wh_circ
        dps = rps * 360
        return dps

    def set_linear_speed(self, speed_ms):
        dps = self.get_linear_dps(speed_ms)

        self.set_left_dps(dps)
        self.set_right_dps(dps)

    def set_turn_speed(self, turn_dps):
        turn_rps = turn_dps / 360
        lin_ms = turn_rps * self.bd_circ
        rps = lin_ms / self.wh_circ
        dps = rps * 360

        self.set_left_dps(dps)
        self.set_right_dps(-dps)

    def reset(self):
        self.BP.reset_all()
        self.ldps = 0
        self.rdps = 0

    def get_linear_degrees(self, length_m, speed_ms=10):
        rotations = length_m / self.wh_circ
        degrees = rotations * 360
        if speed_ms < 0:
            degrees *= -1

        return degrees

    def move_linear(self, length_m, speed_ms=10):
        if length_m < 0:
            length_m *= -1
            speed_ms *= -1

        degrees = self.get_linear_degrees(length_m, speed_ms)
        if degrees != 0:
            self.set_linear_speed(speed_ms)
            self.wait_x_degrees(degrees)

        self.set_linear_speed(0)

    def get_turn_degrees(self, degrees, turn_dps=90):
        turn_rotations = degrees / 360
        linear_length = turn_rotations * self.bd_circ
        wheel_rotations = linear_length / self.wh_circ
        wheel_degrees = wheel_rotations * 360
        if turn_dps < 0:
            wheel_degrees *= -1

        return wheel_degrees

    def turn(self, degrees, turn_dps=90):
        if degrees < 0:
            degrees *= -1
            turn_dps *= -1

        wheel_degrees = self.get_turn_degrees(degrees, turn_dps)
        if wheel_degrees != 0:
            self.set_turn_speed(turn_dps)
            self.wait_x_degrees(wheel_degrees)

        self.set_linear_speed(0)

    def wait_x_degrees(self, degrees):
        degrees_remaining = abs(degrees)
        sign = degrees / degrees_remaining

        last_rot = self.get_left_rot()
        while degrees_remaining > 0:
            current_rot = self.get_left_rot()
            delta = current_rot - last_rot
            degrees_remaining -= delta * sign
            last_rot = current_rot

    def steer(self, speed_ms, turn_amount):
        turn_abs = abs(turn_amount)
        dps = self.get_linear_dps(speed_ms)
        fast_dps = dps * (1 + turn_abs)
        slow_dps = dps * (1 - turn_abs)

        if turn_amount > 0:
            self.set_left_dps(fast_dps)
            self.set_right_dps(slow_dps)
        else:
            self.set_left_dps(slow_dps)
            self.set_right_dps(fast_dps)
