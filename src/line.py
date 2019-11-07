import math
import vector2


class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def sqr_magnitude(self):
        x_dist = self.end_point.x - self.start_point.x
        y_dist = self.end_point.y - self.start_point.y
        return x_dist * x_dist + y_dist * y_dist

    def magnitude(self):
        return math.sqrt(self.sqr_magnitude())

    def angle_rads(self):
        x_dist = self.end_point.x - self.start_point.x
        y_dist = self.end_point.y - self.start_point.y
        return math.degrees(math.atan2(y_dist, x_dist))

    def __eq__(self, other):
        return self.start_point == other.start_point and self.end_point == other.end_point

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.start_point, self.end_point
