import random
import math


def straightLineWeightedParticles(x, y, theta, xdistance, ydistance, sdx, sdy, sdtheta):
    """sdx == sdy?

    """
    newx = x + ((xdistance + random.gauss(0, sdx)) * math.cos(theta))
    newy = y + ((ydistance + random.gauss(0, sdy)) * math.sin(theta))
    newtheta = theta + random.gauss(0, sdtheta)

    newtheta = normaliseAngle(newtheta)

    return newx, newy, newtheta


def rotationWeightedParticles(x, y, theta, turnangle, sdtheta):

    newx = x
    newy = y
    newtheta = theta + turnangle + random.gauss(0, sdtheta)

    newtheta = normaliseAngle(newtheta)

    return newx, newy, newtheta


def normaliseAngle(angle):
    """
    For now we need to make sure that angle is never bigger than pi

    parameters: 
        --angle - angle between -3pi and 3pi
    returns: 
        --angle - modified angle between -pi and pi
    """
    if(angle > (math.pi)):
        return angle - 2*(math.pi)
    elif(angle < -(math.pi)):
        return angle + 2*(math.pi)
    else:
        return angle


if __name__ == "__main__":
    straightLineWeightedParticles(0, 0, 0, 1, 0.2, 0.3, 0.1, 100)
    # rotationWeightedParticles(0, 0, 0, 360, 0.2, 100) # wrong number of arguments
