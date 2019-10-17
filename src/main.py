import movement, brickpi3, time

port_left = brickpi3.BrickPi3.PORT_D
port_right = brickpi3.BrickPi3.PORT_A
wheel_radius = 3.5
body_radius = 6
robot = movement.MovementModule(port_left, port_right, wheel_radius, body_radius)

try:
    robot.set_linear_speed(1)
    time.sleep(2)
    robot.reset()
except KeyboardInterrupt:
    robot.reset()
    
    
