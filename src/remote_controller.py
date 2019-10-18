import keyboard
import movement, brickpi3
import curses

#this script can only be run as root
port_left = brickpi3.BrickPi3.PORT_D
port_right = brickpi3.BrickPi3.PORT_A
wheel_radius = 3.5 / 100 # 3.5cm
body_radius = 9.1 / 100 # 9.1cm
robot = movement.MovementModule(port_left, port_right, wheel_radius, body_radius)


def main(stdscr):
    # do not wait for input when calling getch
    stdscr.nodelay(1)

    while True:
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        if c != -1:
            print('value of c ')
            print(c)
            
            if c == 259: #up arrow
                 robot.set_linear_speed(-10)
            elif c == 258: #down arrow
                robot.set_linear_speed(10)
            elif c == 32: #space bar
                robot.set_linear_speed(0)
                
            if c == 261: #right arrow
                robot.set_turn_speed(-360)
            elif c == 260: #left arrow
                robot.set_turn_speed(360)
            elif c == 32: #space bar
                robot.set_turn_speed(0)
                
                
            
                              
            # print numeric value
            stdscr.addstr(str(c) + ' ')
            stdscr.refresh()
            # return curser to start position
            stdscr.move(0, 0)

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        robot.reset() 
    
    
def depr():
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
