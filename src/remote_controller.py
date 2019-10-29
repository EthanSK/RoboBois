import keyboard
import movement
import brickpi3
import curses
import sounds
from enum import Enum


# this script can only be run as root
port_left = brickpi3.BrickPi3.PORT_D
port_right = brickpi3.BrickPi3.PORT_A
wheel_radius = 3.5 / 100  # 3.5cm
body_radius = 9.1 / 100  # 9.1cm
robot = movement.MovementModule(
    port_left, port_right, wheel_radius, body_radius)


class MovementState(Enum):
    NONE = 0
    FORWARD = 1
    BACKWARD = 2
    CLOCKWISE = 3
    ANTICLOCKWISE = 4


def main(stdscr):
    # do not wait for input when calling getch
    stdscr.nodelay(1)
    lin_speed = 0.05
    turn_speed = 90
    steer_amount = 0
    steer_step = 0.1
    steer_init_step = 0.3
    movement = MovementState.NONE

    while True:
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        if c != -1:
            print('value of c ')
            print(c)
            # 49 is 1 in ascii
            if c >= 49 and c <= 53:
                lin_speed = c - 49
                lin_speed = 0.05 + lin_speed / 15
                if movement == MovementState.FORWARD:
                    robot.steer(-lin_speed, steer_amount)
                elif movement == MovementState.BACKWARD:
                    robot.steer(lin_speed, steer_amount)

            if c >= 54 and c <= 57:
                turn_speed = c - 54
                turn_speed = 8 + turn_speed * 30
                if movement == MovementState.CLOCKWISE:
                    robot.set_turn_speed(-turn_speed)
                elif movement == MovementState.ANTICLOCKWISE:
                    robot.set_turn_speed(turn_speed)

            lin_speed_mul = -1 if movement is MovementState.FORWARD else 1

            if c == 259:  # up arrow
                steer_amount = 0
                robot.steer(-lin_speed, steer_amount)
                movement = MovementState.FORWARD
            elif c == 258:  # down arrow
                steer_amount = 0
                robot.steer(lin_speed, steer_amount)
                movement = MovementState.BACKWARD

            elif c == 32:  # space bar
                steer_amount = 0
                robot.set_linear_speed(0)
                movement = MovementState.NONE

            elif c == 261:  # right arrow
                if movement is MovementState.FORWARD or movement is MovementState.BACKWARD:
                    if steer_amount is 0: steer_amount = steer_init_step
                    else: steer_amount = min(1, steer_amount + steer_step)
                    robot.steer(lin_speed * lin_speed_mul, steer_amount)
                else:
                    robot.set_turn_speed(-turn_speed)
                    movement = MovementState.CLOCKWISE
            elif c == 260:  # left arrow
                if movement is MovementState.FORWARD or movement is MovementState.BACKWARD:
                    if steer_amount is 0: steer_amount = -steer_init_step
                    else: steer_amount = max(-1, steer_amount - steer_step)
                    robot.steer(lin_speed * lin_speed_mul, steer_amount)
                else:
                    robot.set_turn_speed(turn_speed)
                    movement = MovementState.ANTICLOCKWISE

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
