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
touch_port_left = brickpi3.BrickPi3.PORT_4
touch_port_right = brickpi3.BrickPi3.PORT_3
sonar_port = brickpi3.BrickPi3.PORT_2
sonar_motor_port = brickpi3.BrickPi3.PORT_C

wheel_radius = 3.5  # 3.5cm
body_radius = 8  # cm #works on carpet at 8.4


BP = brickpi3.BrickPi3()
BP.reset_all()

movement_module = movement.MovementModule(
    BP, motor_port_left, motor_port_right, wheel_radius, body_radius)

sensor_module = sensor.SensorModule(
    BP, touch_port_left, touch_port_right, sonar_port, sonar_motor_port)

roboboi = robot.Robot(BP, movement_module, sensor_module)

roboboi.force_pos_rot(Vector2(84, 30), 0)


def montecarlo_run():
    # old waypoints follow
    split = map_data.split_path(map_data.waypoints, 10)
    for point in split:
        roboboi.move_to_pos(point, 20, 45, True)
        roboboi.particles.draw()
        time.sleep(0.4)


if __name__ == "__main__":
    try:
        montecarlo.draw_lines()
        walls = map_data.generate_map().convert_walls_to_lines()
        # don't make the spacing more than the bottle radius!
        occ_map = occupancy_map.OccupancyMap(walls, 5)
        occ_map.draw_grid(canvas)
        # canvas.drawParticles(
        #     [Particle(85, 65, 0, 0.5)])

        roboboi.find_bottles(
            occ_map, 10, 20, 45)

        roboboi.reset()

    except KeyboardInterrupt:
        roboboi.reset()
