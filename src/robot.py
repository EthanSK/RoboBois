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

    def find_bottles_mk2(self, _map, speed=20, turn_speed=45, move_bottle_speed=5):
        #area_centers_abc = [Vector2(168, 42), Vector2(126,147), Vector2(42,112)] #[a, b, c]
        area_points_abc = [Vector2(168, 42), Vector2(145,147), Vector2(42,112)] #[a, b, c]
        #area_entrances_and_angles = [(Vector2(126, 42), (-45, 45), (0)), (Vector2(126,84), (-35, 35), (90)), (Vector2(84,84), (-60, 40), (135)) ]
        def move_back_a_bit():
            #print("pos before moving back: ", self.pos)
            dist = -10
            self.movement_module.move_linear(dist, move_bottle_speed, None, False) # no bump detection
            #update position!!!
            self.pos = self.pos + Vector2(dist * math.cos(math.radians(self.rot)), dist * math.sin(math.radians(self.rot)))
            #print("pos after moving back", self.pos)
        def move_to_map_center():
            map_data.draw_pos_rot(self.pos, self.rot, 6, canvas)           
            self.move_to_pos(Vector2(126, 80), speed, turn_speed, False, False)
            pass
        arr = area_points_abc
        for i in range(len(arr)):
            point = area_points_abc[i]
            #point = data[0]
            #angles = data[1]
            #start_angle_at_entrance = data[2]
            #pos_arr = [area_center, area_center + Vector2(0,20), area_center - Vector2(0, 20)] # off for now
            for pos in [point]:
                # moves to current pos first loop iter
                did_fully_move = self.move_to_pos(pos, speed, turn_speed, False, True) #has bump detection
                if not did_fully_move:
                    #then it bumped into a bottle. we can count this as a success and move to the next one
                    print("did not fully move")
                    move_back_a_bit()
                    if i == len(arr) - 1: return
                    move_to_map_center()
                    break
                #self.movement_module.turn(self.rot - start_angle_at_entrance ,turn_speed)
                #self.rot = start_angle_at_entrance
                self.draw_pos()
                #if point.x == 126: exit()
                found_and_bumped_bottle = False
                while not found_and_bumped_bottle:
                    time.sleep(0.5) #let it decelerate
                    if self.sensor_module.get_right_touch() or self.sensor_module.get_left_touch():
                        #is hitting bottle
                        print("hit bottle while decelerating")
                        found_and_bumped_bottle = True
                        move_back_a_bit()
                        if i == len(arr) - 1: return
                        move_to_map_center()
                        continue
                    scan_res = self.sensor_module.get_sonar_full_rotation(
                       5, 0.02, True, self.pos, self.rot)
                    #scan_res = self.sensor_module.get_sonar_rotation_between(angles[0], angles[1],  1, 0.02, True, self.pos, self.rot)
                    #sometimes due to slight deceleration it can move a little bit aftert stopping move_to_pos. Therefore we should check the bump sensors again

                    min_dist = math.inf
                    pos_to_use = Vector2(0,0)
                    dist_wall = 0
                    for data in scan_res:
                        angle_rel_robot = data[0]
                        actual_dist = data[1]
                        absolute_angle = angle_rel_robot + self.rot
                        wall, expected_dist = find_nearest_wall(self.pos.x, self.pos.y, absolute_angle, _map)
                        dist_diff = expected_dist - actual_dist # not abs, it should only work if it's shorter dist that it thought
                        #print(" actual dist: ", actual_dist, "angle abs: ", absolute_angle)
                        potential_pos = Vector2(actual_dist * math.cos(math.radians(absolute_angle)), actual_dist * math.sin(math.radians(absolute_angle))) + self.pos
                        walls_as_lines = _map.convert_walls_to_lines()                        
                        #check potential pos dist to wall, and don't consider it if it's within 20cm
                        potential_bottle_to_wall_distance = map_data.nearest_line_to_point_dist(potential_pos, walls_as_lines)
                        #print("potential bottle dist to nearest wall: ", potential_bottle_to_wall_distance)
                        if actual_dist < min_dist: 
                            min_dist = actual_dist
                            pos_to_use = potential_pos
                            dist_wall = potential_bottle_to_wall_distance
                    bottle_pos = pos_to_use
                    print("bottle_pos: ", bottle_pos, "robot pos: ", self.pos, "dist_wall: ", dist_wall)
                    
                    map_data.draw_pos(bottle_pos, 6, canvas)
                    did_fully_move = self.move_to_pos(bottle_pos, move_bottle_speed, turn_speed, False, True) #has bump detection
                    if not did_fully_move:
                        #then it bumped into a bottle. we can count this as a success and move to the next one
                        print("found bottle normally")                        
                        move_back_a_bit()
                        if i == len(arr) - 1: return
                        move_to_map_center()
                        found_and_bumped_bottle = True
                        
                

                
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


    def move_to_pos(self, pos, speed_m=20, turn_speed=45, should_use_montecarlo=False, with_bump_detection=False):
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
            self.draw_pos()
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

    def draw_pos(self):
        map_data.draw_pos_rot(self.pos,self.rot, 4, canvas)