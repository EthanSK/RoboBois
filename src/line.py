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

    def angle(self):
        return math.degrees(self.angle_rads())

    def angle_rads(self):
        return (self.end_point - self.start_point).angle_rads()

    def overlaps_point(self, point):
        # a + b = c
        # a^2 + 2sqrt(a^2 * b^2) + b^2 = c^2
        a2 = (point - self.start_point).sqr_magnitude()
        b2 = (point - self.end_point).sqr_magnitude()
        c2 = self.sqr_magnitude()
        return math.isclose(a2 + 2 * math.sqrt(a2 * b2) + b2, c2)

    def bounds_point(self, point):
        epsilon = 0.001
        if point.x > max(self.start_point.x, self.end_point.x) + epsilon:
            return False
        if point.x < min(self.start_point.x, self.end_point.x) - epsilon:
            return False
        if point.y > max(self.start_point.y, self.end_point.y) + epsilon:
            return False
        if point.y < min(self.start_point.y, self.end_point.y) - epsilon:
            return False
        return True

    def __eq__(self, other):
        return self.start_point == other.start_point and self.end_point == other.end_point

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "start point: " + str(self.start_point) + ", end point: " + str(self.end_point)
