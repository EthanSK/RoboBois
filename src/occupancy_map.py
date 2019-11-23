import particleDataStructures
from particleDataStructures import Particle
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class VoxelOccupancyMap(Particle):
    def __init__(self, x, y, weight, is_wall):
        super().__init__(x, y, 0, weight)
        self.is_wall = is_wall


class OccupancyMap:
    def __init__(self, walls, spacing_cm=1):
        self.voxels = []
        self.walls = walls
        self.spacing_cm = spacing_cm
        self.build_grid()

    def build_grid(self):
        # get longest width and height of map, scan through row by row, spawning particles if the index row and col are in or on the walls
        biggest_x, biggest_y = self.get_biggest_dimensions()
        map_as_polygon = self.map_as_polygon()
        for y in range(0, biggest_y + 1, self.spacing_cm):
            for x in range(0, biggest_x + 1, self.spacing_cm):
                # check if coordinate is in map
                is_wall = not map_as_polygon.contains(Point(x, y))
                voxel = VoxelOccupancyMap(
                    x, y, 1 if is_wall else 0.5, is_wall)
                self.voxels.append(voxel)

    def map_as_polygon(self):
        map_points = []
        for wall in self.walls:
            map_points.append((wall.start_point.x, wall.start_point.y))
            map_points.append((wall.end_point.x, wall.end_point.y))

        # map_points.append((self.walls[0].start_point.x, self.walls[0].start_point.y))

        return Polygon(map_points)


# this is currently wrong. it returns the max length of a segment, no the total width and height!! we probably need to manually create the grid. or we could just give it the values lol since we know it

    def get_biggest_dimensions(self):
        biggest_x = 0
        biggest_y = 0
        for wall in self.walls:
            if wall.start_point.x > biggest_x:
                biggest_x = wall.start_point.x
            if wall.end_point.x > biggest_x:
                biggest_x = wall.end_point.x
            if wall.start_point.y > biggest_y:
                biggest_y = wall.start_point.y
            if wall.end_point.y > biggest_y:
                biggest_y = wall.end_point.y

        return (int(biggest_x), int(biggest_y))

    def draw_grid(self, canvas):
        canvas.drawParticles(self.voxels)
