import movement
import sensor
import robot
import brickpi3
import time
import vector2
import weightedParticles

def weightedMovement():

targetPosX = raw_input("X co-ord?")
targetPosY = raw_input("Y co-ord?")

targetPosX = float(targetPosX)
targetPosY = float(targetPosY)

particles = [0,0,0] * 100

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

sum = (0, 0, 0)

for i in range(len(particles)):
    for q in range(3):
        sum += particles[i][q] / len(particles)

roboboi.update_pos(sum[0], sum[1], sum[2])

vector = Vector2(targetPosX, targetPosY)
roboboi.move_to_pos(vector, 0.2, 45)






