import math
import particleDataStructures


def generate_map():
    mymap = particleDataStructures.Map()
    # Definitions of walls
    # a: O to A
    # b: A to B
    # c: C to D
    # d: D to E
    # e: E to F
    # f: F to G
    # g: G to H
    # h: H to O
    mymap.add_wall((0, 0, 0, 168))        # a
    mymap.add_wall((0, 168, 84, 168))     # b
    mymap.add_wall((84, 126, 84, 210))    # c
    mymap.add_wall((84, 210, 168, 210))   # d
    mymap.add_wall((168, 210, 168, 84))   # e
    mymap.add_wall((168, 84, 210, 84))    # f
    mymap.add_wall((210, 84, 210, 0))     # g
    mymap.add_wall((210, 0, 0, 0))        # h
    return mymap


def calculate_likelihood(x, y, theta, z):
    mymap = generate_map()
    nearest_wall = find_nearest_wall(x, y, theta, z, mymap)
    m = calculate_forward_distance_to_wall(x, y, theta, nearest_wall)
    return likelihood(z, m, 0.03, 0.05)


# return (x0, y0, x1, y1)
def find_nearest_wall(x, y, theta, z, map):
    # loop through all the walls, calculate the distance m, and find which m is closest to the sonar measurement
    min_distance = float("inf")
    for wall in map.walls:
        m = calculate_forward_distance_to_wall(x, y, theta, wall)

        if distance < min_distance:
            x_point_on_line = m * math.cos(math.radians(theta))
            y_point_on_line = m * math.sin(math.radians(theta))

            #check if distance actually goes through real wall, not wall of inf len
            if is_point_on_line(wall.line_start, wall.line_end, Vector2(x_point_on_line, y_point_on_line)):
                min_distance = distance
                nearest_wall = wall
    return nearest_wall


# calculates m
def calculate_forward_distance_to_wall(x, y, theta, wall):
    Ax, Ay, Bx, By = wall[0], wall[1], wall[2], wall[3]
    # print("wall: " , wall, theta, x, y)
    numerator = (By - Ay) * (Ax - x) - (Bx - Ax) * (Ay - y)
    denomenator = (By - Ay) * math.cos(math.radians(theta)) - (Bx - Ax) * math.sin(math.radians(theta))
    if denomenator is 0 return float("inf") #fine for now, best if we do proper checks later
    return numerator/denomenator


def likelihood(z, m, sd, offset):
    exponent = (-((z - m) ** 2)) / (2 * sd * sd)
    return math.exp(exponent) + offset

def is_point_on_line(line_start, line_end, point):
    if line_start.x == point.x return line_end.x == point.x
    if line_start.y == point.y return line_end.y == point.y
    return (line_start.x - point.x)*(line_start.y - point.y) == (point.x - line_end.x)*(point.y - line_end.y)