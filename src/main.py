import movement, brickpi3, time

port_left = brickpi3.BrickPi3.PORT_D
port_right = brickpi3.BrickPi3.PORT_A
wheel_radius = 3.5 / 100 # 3.5cm
body_radius = 9.1 / 100 # 9.1cm
robot = movement.MovementModule(port_left, port_right, wheel_radius, body_radius)

try:
    #robot.move_linear(0.05, -100)
    robot.set_linear_speed(1)
    #robot.reset()
except KeyboardInterrupt:
    robot.reset()
    
    
