import random
import math

def straightLineWeightedParticles(x, y, theta, distance, sdx, sdy, sdtheta):
    """sdx == sdy?

    """
    newx = x + ((distance + random.gauss(0, sdx)) * math.cos(theta))
    newy = y + ((distance + random.gauss(0, sdy)) * math.sin(theta))
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
    For now we need to make sure that angle is never bigger than 720
    
    parameters: 
        --angle - angle between -360 and 720
    returns: 
        --angle - modified angle
    """
    if(angle > 360): 
        return angle - 360
    elif(angle < 0): 
        return angle + 360
    else: 
        return angle

if __name__ == "__main__":
    straightLineWeightedParticles(0, 0, 0, 1, 0.2, 0.3, 0.1, 100)
    rotationWeightedParticles(0, 0, 0, 360, 0.2, 100)