import math
import particleDataStructures


def calculate_likelihood(x, y, theta, z):
    nearest_wall = find_nearest_wall(x, y, theta, z, )
    m = calculate_distance()


# return (x0, y0, x1, y1)
def find_nearest_wall(x, y, theta, z, map):
    # loop through all the walls, calculate the distance m, and find which m is closest to the sonar measurement
    min_distance = float("inf")
    for wall in map.walls:
        distance = calculate_distance(x, y, theta, wall)
        if distance < min_distance:
            min_distance = distance
            nearest_wall = wall
    return nearest_wall


# calculates m
def calculate_distance(x, y, theta, wall):
    Ax, Ay, Bx, By = wall[0], wall[1], wall[2], wall[3]
    numerator = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
    denomenator = (By - Ay) * math.cos(theta) - (Bx - Ax) * math.sin(theta)
    return numerator/denomenator
