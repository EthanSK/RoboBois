import movement
import sensor
import robot
import brickpi3
import time
import montecarlo

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

ideal_dist = 0.3

try:
    while True:
        sensor_distance = sensor_module.get_sonar_distance()
        likelihood = montecarlo.calculate_likelihood(
            roboboi.pos.x, roboboi.pos.y, roboboi.rot, sensor_distance)
        print("likelihood: " + likelihood)

except KeyboardInterrupt:
    roboboi.reset()
