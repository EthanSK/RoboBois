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
    BP, touch_port_left, touch_port_right, sonar_port, 5)

roboboi = robot.Robot(BP, movement_module, sensor_module, 500)


try:
    montecarlo.draw_lines()
    # a = montecarlo.find_nearest_wall(84, 30, -45, montecarlo.generate_map())
    # print("walllll: ", a[0], a[1])
    # print("actual sensor reading: ", roboboi.sensor_module.get_sonar_snapshot(10, 1000))
    while True:
        # testing resampling
        # ps = Particles(1000)
        # for i in range(ps.count):
        #     x = random.random() * 100
        #     y = random.random() * 100
        #     ps.data.append(Particle(x, y, 0, 90))

        # for i in range(ps.count):
        #     x = random.random() * 100 + 100
        #     y = random.random() * 100
        #     ps.data.append(Particle(x, y, 0, 10))
        # ps.normalize_weights()
        # ps.resample()
        # ps.draw()
        # break

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
        # [print(w) for w in split]
        roboboi.force_pos_rot(waypoints[0], 0)
        for waypoint in split:
            # print("old pose: ", roboboi.pos, roboboi.rot)

            roboboi.move_to_pos(waypoint, 15, 25)
            # sensor_distance = roboboi.sensor_module.get_sonar_distance()
            # print(sensor_distance)

            print("poo ", waypoint, roboboi.pos, roboboi.rot)
            canvas.drawParticles(roboboi.particles.data)
            # time.sleep(0.5)
        roboboi.reset()
        break


except KeyboardInterrupt:
    roboboi.reset()
