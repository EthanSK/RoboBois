import brickpi3
import movement
import sensor
from vector2 import Vector2
import math
from particleDataStructures import Particles
import weightedParticles as ptcls


class Robot:
    SD_X = 3  # cm
    SD_Y = 3  # cm
    SD_THETA_MOV = 1  # degrees
    SD_THETA_ROT = 4  # degrees

    def __init__(self, movement_module, sensor_module, num_particles=100):
        self.movement_module = movement_module
        self.sensor_module = sensor_module
        self.pos = Vector2(0, 0)
        self.rot = 0
        self.particles = Particles(num_particles)

    def reset(self):
        self.movement_module.reset()
        self.sensor_module.reset()

    def force_pos_rot(self, pos, theta):
        self.pos = pos
        self.rot = theta
        self.particles.init_particles(self.pos, self.rot)

    def move_to_pos(self, pos, speed_m=20, turn_speed=45):
        if pos != self.pos:
            delta = pos - self.pos
            dist = delta.magnitude()
            angle = delta.angle()

            angle_delta = (self.rot - angle) % 360
            if angle_delta != 0:
                if angle_delta > 180:
                    angle_delta -= 360

                self.rotate_particles(angle_delta)
                self.movement_module.turn(angle_delta, turn_speed)
                self.rot = angle

            if dist != 0:
                self.move_particles(delta)
                self.movement_module.move_linear(-dist, speed_m)
                self.pos = pos

            self.update_real_pos()

    def move_particles(self, delta):
        for p in self.particles.data:
            p.pos.x, p.pos.y, p.theta = ptcls.straightLineWeightedParticles(
                p.pos.x, p.pos.y, p.theta, delta.x, delta.y, self.SD_X, self.SD_Y, self.SD_THETA_MOV)

    def rotate_particles(self, delta):
        for p in self.particles.data:
            p.pos.x, p.pos.y, p.theta = ptcls.rotationWeightedParticles(
                p.pos.x, p.pos.y, p.theta, delta, self.SD_THETA_ROT)

    def update_real_pos(self):
        sensor_distance = self.sensor_module.get_sonar_snapshot()
        self.particles.update_weights(sensor_distance)
        self.particles.normalize_weights()

        acc_pos = Vector2(0, 0)
        acc_rot = 0

        for p in self.particles.data:
            acc_pos += p.pos * p.weight
            acc_rot += p.theta * p.weight

        self.pos = acc_pos
        self.rot = acc_rot #dunno if this is right

        self.particles.resample()
