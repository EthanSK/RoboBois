import movement
import sensor
import robot
import brickpi3
import time

motor_port_left = brickpi3.BrickPi3.PORT_D
motor_port_right = brickpi3.BrickPi3.PORT_A
touch_port_left = brickpi3.BrickPi3.PORT_4
touch_port_right = brickpi3.BrickPi3.PORT_1
sonar_port = brickpi3.BrickPi3.PORT_2

wheel_radius = 3.5 / 100 # 3.5cm
body_radius = 6.5 / 100 # cm

movement_module = movement.MovementModule(motor_port_left, motor_port_right, wheel_radius, body_radius)
sensor_module = sensor.SensorModule(touch_port_left, touch_port_right, sonar_port)
roboboi = robot.Robot(movement_module, sensor_module)

ideal_dist = 0.3

try:
    while True:
        distance = roboboi.sensor_module.get_sonar_distance()
        delta = ideal_dist - distance
        roboboi.movement_module.set_linear_speed(delta * 2)
        
        if roboboi.sensor_module.get_left_touch() or roboboi.sensor_module.get_right_touch():
            roboboi.movement_module.move_linear(0.3, 0.2)
            roboboi.movement_module.turn(360)

except KeyboardInterrupt:
    roboboi.reset()
    
    
