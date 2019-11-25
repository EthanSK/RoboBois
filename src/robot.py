import brickpi3
import movement
import sensor
from vector2 import Vector2
import math
from particleDataStructures import Particles, canvas
import weightedParticles as ptcls
from cmath import rect, phase
from math import radians, degrees
import map_data
import time


class Robot:
    SD_X_FIXED = 2  # cm
    SD_Y_FIXED = 2  # cm
    SD_THETA_MOV_FIXED = 3  # degrees
    SD_THETA_ROT_FIXED = 5  # degrees

    SD_X_GROWTH = 0.005  # cm
    SD_Y_GROWTH = 0.005  # cm
    SD_THETA_MOV_GROWTH = 0.05  # degrees
    SD_THETA_ROT_GROWTH = 0.1  # degrees

    def __init__(self, BP, movement_module, sensor_module, num_particles=100):
        self.BP = BP
        self.movement_module = movement_module
        self.sensor_module = sensor_module
        self.pos = Vector2(0, 0)
        self.rot = 0
        self.particles = Particles(num_particles)

    def reset(self):
        self.BP.reset_all()

    def force_pos_rot(self, pos, theta):
        self.pos = pos
        self.rot = theta
        self.particles.init_particles(self.pos, self.rot)

    def find_bottles(self, occupancy_map, pos, chunk_size_cm=10, speed=20, turn_speed=45, should_use_montecarlo=True):
        waypoints = map_data.split_path([self.pos, pos], chunk_size_cm)
        occupancy_map.create_kernel(canvas)
        return
        for point in waypoints:
            # moves to current pos first loop iter
            self.move_to_pos(point, speed, turn_speed, should_use_montecarlo)
            scan_res = self.sensor_module.get_sonar_full_rotation(
                15, 0.01, False, self.pos)

            for reading in scan_res:
                occupancy_map.update_cells_in_beam(
                    self, reading, canvas, False)
                # time.sleep(1.5)
            occupancy_map.draw_grid(canvas)
            return  # for testing

    def move_to_pos(self, pos, speed_m=20, turn_speed=45, should_use_montecarlo=True):
        if pos != self.pos:
            delta = pos - self.pos
            dist = delta.magnitude()
            angle = delta.angle()

            angle_delta = -(angle - self.rot) % 360
            if angle_delta != 0:
                if angle_delta > 180:
                    angle_delta = angle_delta - 360

                self.rotate_particles(angle_delta)
                self.movement_module.turn(angle_delta, turn_speed)
                self.rot = angle
            if dist != 0:
                self.move_particles(delta, dist)
                self.movement_module.move_linear(dist, speed_m)
                self.pos = pos

            if should_use_montecarlo:
                self.update_real_pos()

    def move_particles(self, delta, dist):
        dist_sqrt = math.sqrt(dist)
        sdx = self.SD_X_FIXED + self.SD_X_GROWTH * dist_sqrt
        sdy = self.SD_Y_FIXED + self.SD_Y_GROWTH * dist_sqrt
        sdtheta = self.SD_THETA_MOV_FIXED + self.SD_THETA_MOV_GROWTH * dist_sqrt

        for p in self.particles.data:
            p.pos.x, p.pos.y, p.theta = ptcls.straightLineWeightedParticles(
                p.pos.x, p.pos.y, p.theta, delta.x, delta.y, sdx, sdy, sdtheta)

    def rotate_particles(self, delta):
        delta_sqrt = math.sqrt(abs(delta))
        sdtheta = self.SD_THETA_ROT_FIXED + self.SD_THETA_ROT_GROWTH * delta_sqrt
        for p in self.particles.data:
            p.pos.x, p.pos.y, p.theta = ptcls.rotationWeightedParticles(
                p.pos.x, p.pos.y, p.theta, delta, sdtheta)

    def update_real_pos(self):
        sensor_distance = self.sensor_module.get_sonar_snapshot()
        print("sensor distance: ", sensor_distance)
        self.particles.update_weights(sensor_distance)
        self.particles.normalize_weights()
        self.particles.draw()
        self.particles.resample()

        acc_pos = Vector2(0, 0)

        def mean_angle(deg):
            return degrees(phase(sum(rect(1, radians(d)) for d in deg)/len(deg)))

        for p in self.particles.data:
            acc_pos = acc_pos + p.pos

        self.pos = acc_pos / self.particles.count
        self.rot = mean_angle([p.theta for p in self.particles.data])
 