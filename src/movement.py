import brickpi3, math

class MovementModule:
    def __init__(self, lmotor, rmotor, wh_radius, bd_radius):
        self.BP = brickpi3.BrickPi3()
        self.lmotor = lmotor
        self.rmotor = rmotor

        self.wh_radius = wh_radius
        self.wh_circ = wh_radius * 2 * math.pi

        self.bd_radius = bd_radius
        self.bd_circ = bd_radius * 2 * math.pi

    def set_left_dps(self, dps):
        self.BP.set_motor_power(lmotor, dps)

    def set_right_dps(self, dps):
        self.BP.set_motor_power(rmotor, dps)

    def float_all(self):
        self.BP.set_motor_power(lmotor, BP.MOTOR_FLOAT)
        self.BP.set_motor_power(rmotor, BP.MOTOR_FLOAT)

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
        BP.reset_all()

