import movement
import sensor
import robot
import brickpi3
import time
import montecarlo
from vector2 import Vector2
from particleDataStructures import Particles, canvas, Particle
import random
from main import roboboi
import occupancy_map
import map_data

try:
    montecarlo.draw_lines()
    # res = roboboi.movement_module.move_linear(30, 20, roboboi, True)
    # roboboi.force_pos_rot(Vector2(0, 0), 0)
    # roboboi.move_to_pos(Vector2(-10, 10), 10, 45, False, True)
    # roboboi.movement_module.turn(90)
    roboboi.force_pos_rot(Vector2(180, 45), -90)
    walls = map_data.generate_map().convert_walls_to_lines()
    occ_map = occupancy_map.OccupancyMap(walls, 2)
    occ_map.draw_grid(canvas)

    scan_res = roboboi.sensor_module.get_sonar_full_rotation(
        4, 0.01, False, roboboi.pos)
    for reading in scan_res:
        occ_map.update_cells_in_beam(
            roboboi, reading, canvas, False)
    occ_map.draw_grid(canvas)

    while True:
        pass
        break
    roboboi.reset()

except KeyboardInterrupt:
    roboboi.reset()
