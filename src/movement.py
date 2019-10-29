import brickpi3, math

class MovementModule:
    max_power = 50
    max_dps = 0
    
    def __init__(self, lmotor, rmotor, wh_radius, bd_radius, bias = 0):
        self.BP = brickpi3.BrickPi3()
        self.lmotor = lmotor
        self.rmotor = rmotor

        self.wh_radius = wh_radius
        self.wh_circ = wh_radius * 2 * math.pi

        self.bd_radius = bd_radius
        self.bd_circ = bd_radius * 2 * math.pi

        self.bias = bias

    def set_left_dps(self, dps):
        self.BP.set_motor_limits(self.lmotor, MovementModule.max_power, MovementModule.max_dps)
        self.BP.set_motor_dps(self.lmotor, dps)

    def set_right_dps(self, dps):
        self.BP.set_motor_limits(self.rmotor, MovementModule.max_power, MovementModule.max_dps)
        self.BP.set_motor_dps(self.rmotor, dps * (1 + self.bias))

    def get_left_rot(self):
        return self.BP.get_motor_encoder(self.lmotor)

    def get_right_rot(self):
        return self.BP.get_motor_encoder(self.rmotor)

    def float_all(self):
        self.BP.set_motor_power(self.motor, BP.MOTOR_FLOAT)
        self.BP.set_motor_power(self.rmotor, BP.MOTOR_FLOAT)

    def set_linear_speed(self, speed_ms):
        rps = speed_ms / self.wh_circ
        dps = rps * 360

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

    def move_linear(self, length_m, speed_ms = 1):
        rotations = length_m / self.wh_circ
        degrees = rotations * 360
        if speed_ms < 0:
            degrees *= -1

        self.set_linear_speed(speed_ms)
        self.wait_x_degrees(degrees)
        self.set_linear_speed(0)

    def turn(self, degrees, turn_dps = 90):
        turn_rotations = degrees / 360
        linear_length = turn_rotations * self.bd_circ
        wheel_rotations = linear_length / self.wh_circ
        wheel_degrees = wheel_rotations * 360
        if turn_dps < 0:
            wheel_degrees *= -1

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
