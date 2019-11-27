import movement
import sensor
import robot
import brickpi3
import time
import montecarlo
from vector2 import Vector2
from particleDataStructures import Particles, canvas, Particle
import random
from main import roboboi, montecarlo_run
import occupancy_map
import map_data
from montecarlo import find_nearest_wall


try:
    montecarlo.draw_lines()
    _map = map_data.generate_map()
    # montecarlo_run()
    # res = roboboi.movement_module.move_linear(30, 20, roboboi, True)
    #roboboi.force_pos_rot(Vector2(84, 30), 90)
    # roboboi.move_to_pos(Vector2(-10, 10), 10, 45, False, True)
    # roboboi.movement_module.turn(90, 30)

    # roboboi.force_pos_rot(Vector2(100, 45), 0)
    # walls = map_data.generate_map().convert_walls_to_lines()
    # occ_map = occupancy_map.OccupancyMap(walls, 2)
    # occ_map.draw_grid(canvas)

    # scan_res = roboboi.sensor_module.get_sonar_full_rotation(
    #   5, 0.02, True, roboboi.pos, roboboi.rot)
    # for reading in scan_res:
    #    occ_map.update_cells_in_beam(
    #       roboboi, reading, canvas, False)
    # occ_map.draw_grid(canvas)=
    # wall, dist = find_nearest_wall(189, 42, -58, _map)
    # print("wall: ", wall, "dist: ", dist)
    roboboi.sensor_module.get_sonar_rotation_between(-50, 20)
    #roboboi.movement_module.turn_to_angle(roboboi.rot, 69)

    while True:
        pass
        break
    roboboi.reset()

except KeyboardInterrupt:
    roboboi.reset()
