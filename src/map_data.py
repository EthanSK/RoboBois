import particleDataStructures
from vector2 import Vector2


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
