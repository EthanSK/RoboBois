import particleDataStructures
from vector2 import Vector2
from line import Line
import math

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


waypoints = [
    Vector2(84, 30),
    Vector2(180, 30),
    Vector2(180, 54),
    Vector2(138, 54),
    Vector2(138, 168),
    Vector2(114, 168),
    Vector2(114, 84),
    Vector2(84, 84),
    Vector2(84, 30)
]


def split_path(waypoints, split_dist):
    new_points = []
    for i in range(len(waypoints) - 1):
        start = waypoints[i]
        end = waypoints[i + 1]
        delta = end - start
        path_dist = delta.magnitude()
        split_delta = delta.normalized() * split_dist
        split_count = int(path_dist // split_dist)
        for i in range(split_count + 1):
            new_points.append(start + split_delta * i)

    new_points.append(waypoints[-1])
    return new_points


def draw_pos(pos, size, canvas):
    line1 = Line(pos, pos + Vector2(size, size))
    line2 = Line(pos, pos + Vector2(size, -size))
    line3 = Line(pos, pos + Vector2(-size, size))
    line4 = Line(pos, pos + Vector2(-size, -size))
    canvas.draw_line_from_obj(line1)
    canvas.draw_line_from_obj(line2)
    canvas.draw_line_from_obj(line3)
    canvas.draw_line_from_obj(line4)

def draw_pos_rot(pos,rot_degrees, size, canvas):
    arrow_tip = pos + Vector2(size * math.cos(math.radians(rot_degrees)), size * math.sin(math.radians(rot_degrees)))
    head_size = size / 2
    right_arrow_head_end = arrow_tip + Vector2(head_size * math.cos(math.radians(rot_degrees + 135)), head_size * math.sin(math.radians(rot_degrees + 135)))
    left_arrow_head_end = arrow_tip + Vector2(head_size * math.cos(math.radians(rot_degrees - 135)), head_size * math.sin(math.radians(rot_degrees - 135)))
    line1 = Line(pos, arrow_tip)
    line2 = Line(arrow_tip, right_arrow_head_end)
    line3 = Line(arrow_tip, left_arrow_head_end)
    canvas.draw_line_from_obj(line1)
    canvas.draw_line_from_obj(line2)
    canvas.draw_line_from_obj(line3)