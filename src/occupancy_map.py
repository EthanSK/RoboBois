import particleDataStructures


class OccupancyMap:
    def __init__(self, walls, spacing_cm=1):
        self.particles = []
        self.walls = walls
        self.spacing_cm = spacing_cm
        self.build_grid()

    def build_grid(self):
        # get longest width and height of map, scan through row by row, spawning particles if the index row and col are in or on the walls
        biggest_width, biggest_height = self.get_biggest_dimensions()

    def get_biggest_dimensions(self):
        biggest_width = 0
        biggest_height = 0
        for wall in self.walls:
            magnitude = wall.magnitude
            if wall.angle() == 0 or wall.angle() == 180 and magnitude > biggest_width:
                biggest_width = magnitude
            if wall.angle() == 90 or wall.angle() == 270 and magnitude > biggest_height:
                biggest_height = magnitude
        return (biggest_width, biggest_height)

    def draw_grid(self):
        pass
