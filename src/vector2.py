import math


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def sqr_magnitude(self):
        return self.x * self.x + self.y * self.y

    def magnitude(self):
        return math.sqrt(self.sqr_magnitude())

    def angle(self):
        return math.degrees(math.atan2(self.y, self.x))

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
