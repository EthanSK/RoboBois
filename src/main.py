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
motor_port_left = brickpi3.BrickPi3.PORT_D
motor_port_right = brickpi3.BrickPi3.PORT_A
touch_port_left = brickpi3.BrickPi3.PORT_4
touch_port_right = brickpi3.BrickPi3.PORT_3
sonar_port = brickpi3.BrickPi3.PORT_2
sonar_motor_port = brickpi3.BrickPi3.PORT_C

wheel_radius = 3.5  # 3.5cm
body_radius = 8.4  # cm #works on carpet at 8.4


BP = brickpi3.BrickPi3()
# BP.reset_all()

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

try:
    montecarlo.draw_lines()
    # full_rot = roboboi.sensor_module.get_sonar_full_rotation()
    # print(full_rot)

    signatures = place_recog.SignatureContainer(5)
    signatures.delete_loc_files()  # delete from previous runs

    # yes this is not nice and oop, i'm just lazy and using his code.
    place_recog.learn_location(roboboi, signatures, False)
    # place_recog.recognize_location()

    roboboi.reset()

except KeyboardInterrupt:
    roboboi.reset()
