import movement
import sensor
import robot
import brickpi3
import time
import montecarlo
from vector2 import Vector2
from particleDataStructures import Particles


motor_port_left = brickpi3.BrickPi3.PORT_D
motor_port_right = brickpi3.BrickPi3.PORT_A
touch_port_left = brickpi3.BrickPi3.PORT_4
touch_port_right = brickpi3.BrickPi3.PORT_1
sonar_port = brickpi3.BrickPi3.PORT_2

wheel_radius = 3.5 / 100  # 3.5cm
body_radius = 6.5 / 100  # cm

movement_module = movement.MovementModule(
    motor_port_left, motor_port_right, wheel_radius, body_radius)
sensor_module = sensor.SensorModule(
    touch_port_left, touch_port_right, sonar_port)
roboboi = robot.Robot(movement_module, sensor_module)
roboboi.pos = Vector2(10, 10)
roboboi.rot = 45

particles = Particles(10)

try:
    while True:
        sensor_distance = sensor_module.get_sonar_distance()
        particles.update_weights(sensor_distance)
        particles.normalize_weights()
        particles.resample()
        # likelihood = montecarlo.calculate_likelihood(
        #     roboboi.pos.x, roboboi.pos.y, roboboi.rot, sensor_distance)
        # print("likelihood: ", likelihood, "\n")

except KeyboardInterrupt:
    roboboi.reset()
