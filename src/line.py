import math
import vector2


class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def sqr_magnitude(self):
        return (self.end_point - self.start_point).sqr_magnitude()

    def magnitude(self):
        return math.sqrt(self.sqr_magnitude())

    def angle_rads(self):
        return (self.end_point - self.start_point).angle()

    def overlaps_point(self, point):
        return math.isclose(self.magnitude(), (point - self.start_point).magnitude() + (point - self.end_point).magnitude())

    def __eq__(self, other):
        return self.start_point == other.start_point and self.end_point == other.end_point

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "start point: " + str(self.start_point) + ", end point: " + str(self.end_point)
