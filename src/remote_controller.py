import keyboard
import movement, brickpi3

#this script can only be run as root
port_left = brickpi3.BrickPi3.PORT_D
port_right = brickpi3.BrickPi3.PORT_A
wheel_radius = 3.5 / 100 # 3.5cm
body_radius = 9.1 / 100 # 9.1cm
robot = movement.MovementModule(port_left, port_right, wheel_radius, body_radius)
try:
    while True:
        try:
            if keyboard.is_pressed('up arrow'):
                #print('up arrow pressed')
                robot.set_linear_speed(-5)
            elif keyboard.is_pressed('down arrow'):
                robot.set_linear_speed(5)
            else:
                robot.set_linear_speed(0)
                
            if keyboard.is_pressed('right arrow'):
                robot.set_turn_speed(720)
            elif keyboard.is_pressed('left arrow'):
                robot.set_turn_speed(-720)
            else:
                robot.set_turn_speed(0)
                
        except Exception as e:
            print(e)
            break
except KeyboardInterrupt:
    robot.reset()