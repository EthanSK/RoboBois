import movement
import sensor
import robot
import brickpi3
import time
import montecarlo
from vector2 import Vector2
from particleDataStructures import Particles, canvas, Particle
import random
import place_recog


# this script can only be run as root
motor_port_left = brickpi3.BrickPi3.PORT_A
motor_port_right = brickpi3.BrickPi3.PORT_D
touch_port_left = brickpi3.BrickPi3.PORT_4
touch_port_right = brickpi3.BrickPi3.PORT_3
sonar_port = brickpi3.BrickPi3.PORT_2
sonar_motor_port = brickpi3.BrickPi3.PORT_C

wheel_radius = 3.5  # 3.5cm
body_radius = 8.4  # cm #works on carpet at 8.4


BP = brickpi3.BrickPi3()
BP.reset_all()

movement_module = movement.MovementModule(
    BP, motor_port_left, motor_port_right, wheel_radius, body_radius)

sensor_module = sensor.SensorModule(
    BP, touch_port_left, touch_port_right, sonar_port, sonar_motor_port)

roboboi = robot.Robot(BP, movement_module, sensor_module)

waypoints = [
    Vector2(84, 30),
    Vector2(180, 30),
    Vector2(180, 54),
    Vector2(138, 54),
    Vector2(138, 168),
    Vector2(114, 168),
    Vector2(114, 84),
    Vector2(84, 84),
    Vector2(84, 30)
]
if __name__ == "__main__":
    try:
        montecarlo.draw_lines()

        # while True:
        #     full_rot = roboboi.sensor_module.get_sonar_full_rotation(
        #         1, 0.004, True, (180, 30))
        #     print(full_rot)

        # input("set in location to guess (Press Enter when ready)")
        # res = place_recog.recognize_location(roboboi, signatures, False)
        # print("location index: ", res[0], "angle shift: ", res[1])
        # while True:
        #     dist = roboboi.sensor_module.get_sonar_distance()
        #     print(dist)

        roboboi.reset()

    except KeyboardInterrupt:
        roboboi.reset()
