import keyboard
import movement
import sensor
import robot
import brickpi3
import curses
import sounds
from enum import Enum


# this script can only be run as root
motor_port_left = brickpi3.BrickPi3.PORT_D
motor_port_right = brickpi3.BrickPi3.PORT_A
touch_port_left = brickpi3.BrickPi3.PORT_4
touch_port_right = brickpi3.BrickPi3.PORT_1
sonar_port = brickpi3.BrickPi3.PORT_3

wheel_radius = 3.5  # 3.5cm
body_radius = 9.1  # 9.1cm
movement = movement.MovementModule(
    motor_port_left, motor_port_right, wheel_radius, body_radius)
sensor_module = sensor.SensorModule(touch_port_left, touch_port_right, sonar_port)
roboboi = robot.Robot(movement, sensor_module)



class MovementState(Enum):
    NONE = 0
    FORWARD = 1
    BACKWARD = 2
    CLOCKWISE = 3
    ANTICLOCKWISE = 4


def main(stdscr):
    # do not wait for input when calling getch
    stdscr.nodelay(1)
    lin_speed = 5
    turn_speed = 90
    steer_amount = 0
    steer_step = 0.1
    steer_init_step = 0.3
    movement_state = MovementState.NONE
    # need_crash_recovery = False

    while True:
        # get keyboard input, returns -1 if none available

        if sensor_module.get_left_touch(): 
            # crash_recovery_routine(lin_speed, turn_speed, -1)
            pass
        if sensor_module.get_right_touch(): 
            # crash_recovery_routine(lin_speed, turn_speed, 1)
            pass

        c = stdscr.getch()
        if c != -1:
            print('value of c ')
            print(c)
            # 49 is 1 in ascii
            if c >= 49 and c <= 53:
                lin_speed = c - 49
                lin_speed = 5 + lin_speed / 0.15
                if movement_state == MovementState.FORWARD:
                    movement.steer(-lin_speed, steer_amount)
                elif movement_state == MovementState.BACKWARD:
                    movement.steer(lin_speed, steer_amount)

            if c >= 54 and c <= 57:
                turn_speed = c - 54
                turn_speed = 8 + turn_speed * 30
                if movement_state == MovementState.CLOCKWISE:
                    movement.set_turn_speed(-turn_speed)
                elif movement_state == MovementState.ANTICLOCKWISE:
                    movement.set_turn_speed(turn_speed)

            lin_speed_mul = -1 if movement_state is MovementState.FORWARD else 1

            if c == 259:  # up arrow
                steer_amount = 0
                movement.steer(-lin_speed, steer_amount)
                movement_state = MovementState.FORWARD
            elif c == 258:  # down arrow
                steer_amount = 0
                movement.steer(lin_speed, steer_amount)
                movement_state = MovementState.BACKWARD

            elif c == 32:  # space bar
                steer_amount = 0
                movement.set_linear_speed(0)
                movement_state = MovementState.NONE

            elif c == 261:  # right arrow
                if movement_state is MovementState.FORWARD or movement_state is MovementState.BACKWARD:
                    if steer_amount is 0: steer_amount = steer_init_step
                    else: steer_amount = min(1, steer_amount + steer_step)
                    movement.steer(lin_speed * lin_speed_mul, steer_amount)
                else:
                    movement.set_turn_speed(-turn_speed)
                    movement_state = MovementState.CLOCKWISE
            elif c == 260:  # left arrow
                if movement_state is MovementState.FORWARD or movement_state is MovementState.BACKWARD:
                    if steer_amount is 0: steer_amount = -steer_init_step
                    else: steer_amount = max(-1, steer_amount - steer_step)
                    movement.steer(lin_speed * lin_speed_mul, steer_amount)
                else:
                    movement.set_turn_speed(turn_speed)
                    movement_state = MovementState.ANTICLOCKWISE

            elif c == 113:  # q
                print("{}cm".format(sensor_module.get_sonar_distance()))

            # print numeric value
            stdscr.addstr(str(c) + ' ')
            stdscr.refresh()
            # return curser to start position
            stdscr.move(0, 0)

def crash_recovery_routine(lin_speed, turn_speed, direction):
    print("crash recovery started")
    ldps = movement.ldps
    rdps = movement.rdps
    movement.move_linear(15, lin_speed)
    movement.turn(25, direction * turn_speed)
    movement.set_left_dps(ldps)
    movement.set_right_dps(rdps)


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        roboboi.reset()
