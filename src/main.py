import movement
import sensor
import robot
import brickpi3
import time
import montecarlo
from vector2 import Vector2
from particleDataStructures import Particles, canvas


motor_port_left = brickpi3.BrickPi3.PORT_D
motor_port_right = brickpi3.BrickPi3.PORT_A
touch_port_left = brickpi3.BrickPi3.PORT_4
touch_port_right = brickpi3.BrickPi3.PORT_1
sonar_port = brickpi3.BrickPi3.PORT_2

wheel_radius = 3.5  # 3.5cm
body_radius = 8.4  # cm #works on carpet at 8.4

movement_module = movement.MovementModule(
    motor_port_left, motor_port_right, wheel_radius, body_radius)
sensor_module = sensor.SensorModule(
    touch_port_left, touch_port_right, sonar_port, 8)
roboboi = robot.Robot(movement_module, sensor_module, 1)



try:
    montecarlo.draw_lines()
    while True:
        # break
        waypoints = [
             (84, 30), (180, 30), (180, 54) ,(138, 54) ,(138, 168), (114, 168), (114, 84) , (84, 84) ,(84, 30)
        ]
        roboboi.force_pos_rot(Vector2(waypoints[0][0], waypoints[0][1]), 0)
        for waypoint in waypoints:
            print("old pose: ", roboboi.pos, roboboi.rot)
            roboboi.move_to_pos(Vector2(waypoint[0], waypoint[1]))
            print("new pose: ", roboboi.pos, roboboi.rot)
            canvas.drawParticles(roboboi.particles.data)


except KeyboardInterrupt:
    roboboi.reset()
