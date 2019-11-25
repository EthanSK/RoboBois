import particleDataStructures
from particleDataStructures import Particle
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from line import Line
from vector2 import Vector2


class CellOccupancyMap(Particle):
    def __init__(self, x, y, weight, is_wall):
        super().__init__(x, y, 0, weight)
        self.is_wall = is_wall


class OccupancyMap:
    BEAM_SPREAD_DEGREES = 10
    VALID_MAX_SONAR_DIST = 100  # after 100cm they become a bit b a d
    SONAR_UNCERTAINTY_CM = 2

    def __init__(self, walls, spacing_cm=1):
        self.cells = []
        self.walls = walls
        self.spacing_cm = spacing_cm
        self.build_grid()

    def build_grid(self):
        biggest_x, biggest_y = self.get_biggest_dimensions()
        map_as_polygon = self.map_as_polygon()
        for y in range(0, biggest_y + 1, self.spacing_cm):
            for x in range(0, biggest_x + 1, self.spacing_cm):
                # check if coordinate is in map
                is_wall = not map_as_polygon.contains(Point(x, y))
                cell = CellOccupancyMap(
                    x, y, 1 if is_wall else 0.5, is_wall)
                self.cells.append(cell)

    def map_as_polygon(self):
        map_points = []
        for wall in self.walls:
            map_points.append((wall.start_point.x, wall.start_point.y))
            map_points.append((wall.end_point.x, wall.end_point.y))
        return Polygon(map_points)

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
        canvas.drawParticles(self.cells)

    def update_cells_in_beam(self, robot, sonar_data, canvas, should_draw=True):
        angle = sonar_data[0] + robot.rot

        dist = sonar_data[1]

        max_angle = angle + self.BEAM_SPREAD_DEGREES / 2
        min_angle = angle - self.BEAM_SPREAD_DEGREES / 2
    
        def update_cell_weight(cell, occupied_or_empty_direction):
            # -1 for more empty, 1 for more full
            # this method of weight keeps weights normalized.
            if occupied_or_empty_direction == 1:
                if cell.weight >= 0.5:
                    cell.weight += (1 - cell.weight)/2
                else:
                    cell.weight *= 2
            if occupied_or_empty_direction == -1:
                if cell.weight <= 0.5:
                    cell.weight /= 2
                else:
                    cell.weight -= 1 - cell.weight

 
        for cell in self.cells:
            if cell.is_wall: continue # we don't wanna update cell walls
            line_to_robot = Line(robot.pos, cell.pos)
            cell_angle = line_to_robot.angle()
            cell_dist = line_to_robot.magnitude()
            phi = abs(angle - cell_angle) % 360
            angle_from_centre_beam = 360 - phi if phi > 180 else phi
    
            if angle_from_centre_beam <= self.BEAM_SPREAD_DEGREES / 2 and cell_dist <= dist + self.SONAR_UNCERTAINTY_CM:
                occupied_or_empty_direction = -1 if cell_dist < dist - self.SONAR_UNCERTAINTY_CM else 1
                if occupied_or_empty_direction == 1 and dist > VALID_MAX_SONAR_DIST: continue #we can't be sure that it's occupied, but we can be sure that cells up to it are empty
                update_cell_weight(cell, occupied_or_empty_direction)
                

        if should_draw:
            robot.sensor_module.draw_sonar_line(
                (max_angle, dist), canvas, robot.pos.x, robot.pos.y)
            robot.sensor_module.draw_sonar_line(
                (min_angle, dist), canvas, robot.pos.x, robot.pos.y)
            # self.draw_grid(canvas)

  
