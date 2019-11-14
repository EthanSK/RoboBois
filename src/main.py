import movement
import sensor
import robot
import brickpi3
import time
import montecarlo
from vector2 import Vector2
from particleDataStructures import Particles, canvas, Particle
import random

motor_port_left = brickpi3.BrickPi3.PORT_D
motor_port_right = brickpi3.BrickPi3.PORT_A
touch_port_left = brickpi3.BrickPi3.PORT_4
touch_port_right = brickpi3.BrickPi3.PORT_1
sonar_port = brickpi3.BrickPi3.PORT_2

wheel_radius = 3.5  # 3.5cm
body_radius = 8.4  # cm #works on carpet at 8.4


BP = brickpi3.BrickPi3()
BP.reset_all()

movement_module = movement.MovementModule(
    BP, motor_port_left, motor_port_right, wheel_radius, body_radius)

sensor_module = sensor.SensorModule(
    BP, touch_port_left, touch_port_right, sonar_port, 7.7)

roboboi = robot.Robot(BP, movement_module, sensor_module, 500)


try:
    montecarlo.draw_lines()

    while True:
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
        split = montecarlo.split_path(waypoints, 20)
        roboboi.force_pos_rot(waypoints[0], 0)
        for waypoint in split:
            roboboi.move_to_pos(waypoint, 12, 25)

            # print("pos ", waypoint, roboboi.pos, roboboi.rot)
            time.sleep(1)
            canvas.drawParticles(roboboi.particles.data)
        roboboi.reset()
        break


except KeyboardInterrupt:
    roboboi.reset()
