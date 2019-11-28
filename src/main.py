import movement
import sensor
import robot
import brickpi3
import time
import montecarlo
import map_data
from vector2 import Vector2
from particleDataStructures import Particles, canvas, Particle
import random
import place_recog
import occupancy_map


# this script can only be run as root
motor_port_left = brickpi3.BrickPi3.PORT_D
motor_port_right = brickpi3.BrickPi3.PORT_A
touch_port_left = brickpi3.BrickPi3.PORT_1
touch_port_right = brickpi3.BrickPi3.PORT_3
sonar_port = brickpi3.BrickPi3.PORT_2
sonar_motor_port = brickpi3.BrickPi3.PORT_C

wheel_radius = 3.5  # 3.5cm
body_radius = 8.6  # cm #works on carpet at 8.6 at turn speed 30


BP = brickpi3.BrickPi3()
time.sleep(0.5)
# BP.reset_all()
time.sleep(0.5)

movement_module = movement.MovementModule(
    BP, motor_port_left, motor_port_right, wheel_radius, body_radius)

sensor_module = sensor.SensorModule(
    BP, touch_port_left, touch_port_right, sonar_port, sonar_motor_port, -1)

roboboi = robot.Robot(BP, movement_module, sensor_module)

roboboi.force_pos_rot(Vector2(84, 30), 0)


def montecarlo_run():
    # old waypoints follow
    split = map_data.split_path(map_data.waypoints, 10)
    for point in map_data.waypoints:
        roboboi.move_to_pos(point, 20, 45, False)
        roboboi.draw_pos()
        time.sleep(0.4)


if __name__ == "__main__":
    try:
        montecarlo.draw_lines()
        # walls = map_data.generate_map().convert_walls_to_lines()
        # don't make the spacing more than the bottle radius!
        # occ_map = occupancy_map.OccupancyMap(walls, 2)
        # occ_map.draw_grid(canvas)
        # canvas.drawParticles(
        #     [Particle(85, 65, 0, 0.5)])
        _map = map_data.generate_map()
        roboboi.find_bottles_mk2(
            _map, 15, 30, 10, 25)
        # we minus 10 because it always overshoots
        roboboi.move_to_pos(
            Vector2(84, 30) + Vector2(-28, 28), 20, 30, False, True)
        roboboi.reset()

    except KeyboardInterrupt:
        roboboi.reset()
