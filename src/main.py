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
roboboi = robot.Robot(movement_module, sensor_module)



try:
    montecarlo.draw_lines()
    
    while True:
        
        waypoints = [
             Vector2(84, 30), Vector2(180, 30), Vector2(180, 54) ,Vector2(138, 54) ,Vector2(138, 168), Vector2(114, 168), Vector2(114, 84) , Vector2(84, 84) ,Vector2(84, 30)
        ]
        split = montecarlo.split_up_waypoints(waypoints, 3)
        # [print(w) for w in split]
        roboboi.force_pos_rot(waypoints[0], 0)
        for waypoint in split:
            # print("old pose: ", roboboi.pos, roboboi.rot)
            roboboi.move_to_pos(waypoint, 15)
            # roboboi.move_to_pos(Vector2(waypoint[0], waypoint[1]), 15)

            # print("new pose: ", roboboi.pos, roboboi.rot)
            canvas.drawParticles(roboboi.particles.data)


except KeyboardInterrupt:
    roboboi.reset()
