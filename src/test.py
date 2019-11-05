import sounds
import brickpi3
import movement
import sensor

motor_port_left = brickpi3.BrickPi3.PORT_D
motor_port_right = brickpi3.BrickPi3.PORT_A
touch_port_left = brickpi3.BrickPi3.PORT_4
touch_port_right = brickpi3.BrickPi3.PORT_1
sonar_port = brickpi3.BrickPi3.PORT_2

wheel_radius = 3.5 / 100  # 3.5cm
body_radius = 9.1 / 100  # 9.1cm
movement = movement.MovementModule(
    motor_port_left, motor_port_right, wheel_radius, body_radius)
sensor_module = sensor.SensorModule(
    touch_port_left, touch_port_right, sonar_port)

movement.move_linear(0.15, -0.1)
