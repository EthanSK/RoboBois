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
import random
from montecarlo import find_nearest_wall


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

    def find_bottles_mk2(self, _map, speed=20, turn_speed=45):
        area_centers_abc = [Vector2(180, 45), Vector2(124,163), Vector2(44,123)] #[a, b, c]
        def move_to_map_center():
            self.move_to_pos(Vector2(105, 105), speed, 45, False, False)
        def move_random():
            # find a random offset to current pos that is not outside (or near the bounds of ) the map
            pass
        for area_center in area_centers_abc:
            pos_arr = [area_center, area_center + Vector2(0,20) , area_center - Vector2(0, 20)] # off for now
            for pos in [area_center]:
                # moves to current pos first loop iter
                did_fully_move = self.move_to_pos(pos, speed, turn_speed, False, True) #has bump detection
                if not did_fully_move:
                    #then it bumped into a bottle. we can count this as a success and move to the next one
                    move_to_map_center()
                    continue
                scan_res = self.sensor_module.get_sonar_full_rotation(
                    10, 0.01, False, self.pos)
                max_diff = 0
                max_diff_angle = 69
                max_diff_dist = 420
                for data in scan_res:
                    angle = data[0]
                    actual_dist = data[1]
                    wall, expected_dist = find_nearest_wall(self.pos.x, self.pos.y, self.rot, _map)
                    dist_diff = expected_dist - actual_dist # not abs, it should only work if it's shorter dist that it thought
                    if dist_diff >= max_diff: 
                        max_diff = dist_diff
                        max_diff_angle = angle
                        max_diff_dist = actual_dist
                move_to_pos = Vector2(max_diff_dist * math.cos(math.radians(max_diff_angle)), max_diff_dist * math.sin(math.radians(max_diff_angle)))
                map_data.draw_pos(move_to_pos, 3, canvas)
                did_fully_move = self.move_to_pos(move_to_pos, speed, turn_speed, False, True) #has bump detection
                if not did_fully_move:
                    #then it bumped into a bottle. we can count this as a success and move to the next one
                    move_to_map_center()
                    continue
                
    def find_bottles(self, occupancy_map, chunk_size_cm=10, speed=20, turn_speed=45):
        area_centers_abc = [Vector2(180, 45), Vector2(124,163), Vector2(44,123)] #[a, b, c]
        # split_waypoints = map_data.split_path([self.pos, pos], chunk_size_cm)
        def move_to_map_center():
            self.move_to_pos(Vector2(105, 105), speed, 45, False, False)
        def move_random():
            # find a random offset to current pos that is not outside (or near the bounds of ) the map
            pass
        for area_center in area_centers_abc:
            pos_arr = [area_center, area_center + Vector2(0,20) , area_center - Vector2(0, 20)] # off for now
            for pos in [area_center]:
                # moves to current pos first loop iter
                did_fully_move = self.move_to_pos(pos, speed, turn_speed, False, True) #has bump detection
                if not did_fully_move:
                    #then it bumped into a bottle. we can count this as a success and move to the next one
                    move_to_map_center()
                    continue
                scan_res = self.sensor_module.get_sonar_full_rotation(
                    int(360 / occupancy_map.BEAM_SPREAD_DEGREES), 0.01, False, self.pos)
                for reading in scan_res:
                    occupancy_map.update_cells_in_beam(
                        self, reading, canvas, False)
                    # time.sleep(1.5)
                occupancy_map.draw_grid(canvas)
            bottle_pos = occupancy_map.detect_bottle_with_kernel()
            map_data.draw_pos(bottle_pos, 3, canvas)
            found_and_bumped_bottle = False
            while not found_and_bumped_bottle:
                if bottle_pos.x != -1:
                    #we found the bottle! move to it and bump
                    self.move_to_pos(bottle_pos, speed, turn_speed, False, True)
                    move_to_map_center()
                    found_and_bumped_bottle = True
                else:
                    #we should move randomly a bit within the area and rescan
                    print("didn't find a bottle so moving randomly")
                    move_random()

                    #this is temp
                    move_to_map_center()
                    break


    def move_to_pos(self, pos, speed_m=20, turn_speed=45, should_use_montecarlo=True, with_bump_detection=False):
        if pos != self.pos:
            delta = pos - self.pos
            dist = delta.magnitude()
            angle = delta.angle()
            angle_rads = delta.angle_rads()

            angle_delta = -(angle - self.rot) % 360
            if angle_delta != 0:
                if angle_delta > 180:
                    angle_delta = angle_delta - 360

                self.rotate_particles(angle_delta)
                self.movement_module.turn(angle_delta, turn_speed)
                self.rot = angle
            if dist != 0:
                len_remaining = self.movement_module.move_linear(dist, speed_m, self, with_bump_detection)
                dist_moved = dist - len_remaining
                real_new_pos = self.pos + Vector2(dist_moved * math.cos(angle_rads), dist_moved * math.sin(angle_rads))

                self.move_particles(delta, dist_moved)
                self.pos = real_new_pos
                print("new pos; ", self.pos)
            if should_use_montecarlo:
                self.update_real_pos()

            return math.isclose(pos.x, self.pos.x) and math.isclose(pos.y, self.pos.y) 

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
