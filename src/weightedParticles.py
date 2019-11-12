import random
import math


def straightLineWeightedParticles(x, y, theta_degrees, xdistance, ydistance, sdx, sdy, sdtheta):

    newx = x + xdistance + (random.gauss(0, sdx) *
                            math.cos(math.radians(theta_degrees)))
    newy = y + ydistance + (random.gauss(0, sdy) *
                            math.sin(math.radians(theta_degrees)))
    newtheta = theta_degrees + random.gauss(0, sdtheta)

    newtheta = normalize_angle(theta_degrees)

    return newx, newy, newtheta


def rotationWeightedParticles(x, y, theta, turnangle, sdtheta):

    newx = x
    newy = y
    newtheta = theta + turnangle + random.gauss(0, sdtheta)

    newtheta = normalize_angle(newtheta)

    return newx, newy, newtheta


def normalize_angle(angle):
   # Make angle between 0 and 360
    angle %= 360

    # Make angle between -179 and 180
    if angle > 180:
        angle -= 360
    return angle
