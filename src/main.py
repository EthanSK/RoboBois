import movement, brickpi3, time

port_left = brickpi3.BrickPi3.PORT_D
port_right = brickpi3.BrickPi3.PORT_A
wheel_radius = 3.5 / 100 # 3.5cm
body_radius = 6.5 / 100 # cm
robot = movement.MovementModule(port_left, port_right, wheel_radius, body_radius)


try:
    for i in range(4):
        robot.move_linear(0.4, -0.1)
        #time.sleep(2)
        robot.turn(90, 40)
        #time.sleep(2)
    robot.reset()

except KeyboardInterrupt:
    robot.reset()
    
    
