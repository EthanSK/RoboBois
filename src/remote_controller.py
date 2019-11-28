import keyboard
import movement
import sensor
import robot
import brickpi3
import curses
import sounds
from enum import Enum
from main import roboboi



class MovementState(Enum):
    NONE = 0
    FORWARD = 1
    BACKWARD = 2
    CLOCKWISE = 3
    ANTICLOCKWISE = 4


def main(stdscr):
    # do not wait for input when calling getch
    stdscr.nodelay(1)
    lin_speed = 12
    turn_speed = 100
    steer_amount = 0
    steer_step = 0.1
    steer_init_step = 0.3
    movement_state = MovementState.NONE
    sonar_rotate_state = 0 #-1 for anticlockwise, 1 for clockwise
    sonar_rotate_multiplier = 3

    while True:
        # get keyboard input, returns -1 if none available

        if roboboi.sensor_module.get_left_touch(): 
            #crash_recovery_routine(-lin_speed, turn_speed, 1)
            pass
        if roboboi.sensor_module.get_right_touch(): 
            #crash_recovery_routine(-lin_speed, turn_speed, -1)
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
                    roboboi.movement_module.steer(-lin_speed, steer_amount)
                elif movement_state == MovementState.BACKWARD:
                    roboboi.movement_module.steer(lin_speed, steer_amount)

            if c >= 54 and c <= 57:
                turn_speed = c - 54
                turn_speed = 8 + turn_speed * 30
                if movement_state == MovementState.CLOCKWISE:
                    roboboi.movement_module.set_turn_speed(turn_speed)
                elif movement_state == MovementState.ANTICLOCKWISE:
                    roboboi.movement_module.set_turn_speed(-turn_speed)
                if sonar_rotate_state != 0:
                    roboboi.sensor_module.BP.set_motor_dps(roboboi.sensor_module.sonar_motor, sonar_rotate_state * turn_speed * sonar_rotate_multiplier)

            lin_speed_mul = -1 if movement_state is MovementState.FORWARD else 1

            if c == 259:  # up arrow
                steer_amount = 0
                roboboi.movement_module.steer(-lin_speed, steer_amount)
                movement_state = MovementState.FORWARD
            elif c == 258:  # down arrow
                steer_amount = 0
                roboboi.movement_module.steer(lin_speed, steer_amount)
                movement_state = MovementState.BACKWARD
            
            elif c == 32:  # space bar
                steer_amount = 0
                roboboi.movement_module.set_linear_speed(0)
                movement_state = MovementState.NONE
                roboboi.sensor_module.BP.set_motor_dps(roboboi.sensor_module.sonar_motor, 0)
                sonar_rotate_state = 0

            elif c == 261:  # right arrow
                if movement_state is MovementState.FORWARD or movement_state is MovementState.BACKWARD:
                    if steer_amount is 0: steer_amount = steer_init_step
                    else: steer_amount = min(1, steer_amount + steer_step)
                    roboboi.movement_module.steer(lin_speed * lin_speed_mul, steer_amount)
                else:
                    roboboi.movement_module.set_turn_speed(turn_speed)
                    movement_state = MovementState.CLOCKWISE
            elif c == 260:  # left arrow
                if movement_state is MovementState.FORWARD or movement_state is MovementState.BACKWARD:
                    if steer_amount is 0: steer_amount = -steer_init_step
                    else: steer_amount = max(-1, steer_amount - steer_step)
                    roboboi.movement_module.steer(lin_speed * lin_speed_mul, steer_amount)
                else:
                    roboboi.movement_module.set_turn_speed(-turn_speed)
                    movement_state = MovementState.ANTICLOCKWISE

            elif c == 113:  # q
                print("{}cm".format(roboboi.sensor_module.get_sonar_distance()))
            elif c == 100 or c == 101: #d or e (to accomodate dvorak)
                roboboi.sensor_module.BP.set_motor_dps(roboboi.sensor_module.sonar_motor, turn_speed * sonar_rotate_multiplier)
                sonar_rotate_state = 1
            elif c == 97: #a
                roboboi.sensor_module.BP.set_motor_dps(roboboi.sensor_module.sonar_motor, -turn_speed * sonar_rotate_multiplier)
                sonar_rotate_state = -1

            # print numeric value
            stdscr.addstr(str(c) + ' ')
            stdscr.refresh()
            # return curser to start position
            stdscr.move(0, 0)

def crash_recovery_routine(lin_speed, turn_speed, direction):
    print("crash recovery started")
    ldps = roboboi.movement_module.ldps
    rdps = roboboi.movement_module.rdps
    roboboi.movement_module.move_linear(15, lin_speed)
    roboboi.movement_module.turn(25, direction * turn_speed)
    roboboi.movement_module.set_left_dps(ldps)
    roboboi.movement_module.set_right_dps(rdps)


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        roboboi.reset()
