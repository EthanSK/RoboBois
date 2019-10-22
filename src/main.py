import movement, brickpi3, time

port_left = brickpi3.BrickPi3.PORT_D
port_right = brickpi3.BrickPi3.PORT_A
wheel_radius = 3.5 / 100 # 3.5cm
body_radius = 7.2 / 100 # 8cm
bisd = 0.2 # 20%
robot = movement.MovementModule(port_left, port_right, wheel_radius, body_radius, bias)

try:
    for i in range(4):
        robot.move_linear(0.4, -0.1)
        robot.turn(90, 40)
    
    robot.reset()

except KeyboardInterrupt:
    robot.reset()
    
    
