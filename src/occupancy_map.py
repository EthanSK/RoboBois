import particleDataStructures
from particleDataStructures import Particle, canvas
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from line import Line
from vector2 import Vector2
import math


class CellOccupancyMap(Particle):
    def __init__(self, x, y, weight, is_wall):
        super().__init__(x, y, 0, weight)
        self.is_wall = is_wall


class OccupancyMap:
    BEAM_SPREAD_DEGREES = 20 #from testing it seems to be huge
    VALID_MAX_SONAR_DIST = 100  # after 100cm they become a bit b a d
    SONAR_UNCERTAINTY_CM = 2
    BOTTLE_DIAMETER_CM = 10
    KERNEL_BORDER_CM = 3
    KERNEL_IGNORE_BORDER_CM = 1 #the ring around the bottle that should be ignored due to inaccuracies
    BOTTLE_DETECTION_MIN_SCORE_OVER_AIR = 3

    def __init__(self, walls, spacing_cm=1):
        self.cells = []
        self.walls = walls
        self.spacing_cm = spacing_cm
        self.kernel = []
        self.build_grid()
        self.create_kernel(canvas, True)

    def build_grid(self):
        biggest_x, biggest_y = self.get_biggest_dimensions()
        map_as_polygon = self.map_as_polygon()
        for i, y in enumerate(range(0, biggest_y + 1, self.spacing_cm)):
            self.cells.append([])
            for x in range(0, biggest_x + 1, self.spacing_cm):
                # check if coordinate is in map
                is_wall = not map_as_polygon.contains(Point(x, y))
                cell = CellOccupancyMap(
                    x, y, 1 if is_wall else 0.5, is_wall)
                self.cells[i].append(cell)

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
        print("drawing grid")
        particles = []
        for cell_row in self.cells:
            particles += cell_row
        canvas.drawParticles(particles)

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

        for cell_row in self.cells:
            for cell in cell_row:
                if cell.is_wall:
                    continue  # we don't wanna update cell walls
                line_to_robot = Line(robot.pos, cell.pos)
                cell_angle = line_to_robot.angle()
                cell_dist = line_to_robot.magnitude()
                phi = abs(angle - cell_angle) % 360
                angle_from_centre_beam = 360 - phi if phi > 180 else phi

                if angle_from_centre_beam <= self.BEAM_SPREAD_DEGREES / 2 and cell_dist <= dist + self.SONAR_UNCERTAINTY_CM:
                    occupied_or_empty_direction = -1 if cell_dist < dist - \
                        self.SONAR_UNCERTAINTY_CM else 1
                    if occupied_or_empty_direction == 1 and dist > self.VALID_MAX_SONAR_DIST:
                        continue  # we can't be sure that it's occupied, but we can be sure that cells up to it are empty 
                    update_cell_weight(cell, occupied_or_empty_direction)

        if should_draw:
            robot.sensor_module.draw_sonar_line(
                (max_angle, dist), canvas, robot.pos.x, robot.pos.y)
            robot.sensor_module.draw_sonar_line(
                (min_angle, dist), canvas, robot.pos.x, robot.pos.y)
            # self.draw_grid(canvas)

    def detect_bottle_with_kernel(self, should_draw = False):
        # 2L coke bottle is 11cm in diameter
        kernel_cell_count_width = len(self.kernel)

        air_score = 0 #score of all cells weight at 0.5 in kernel
        for kernel_y in range(kernel_cell_count_width):
            for kernel_x in range(kernel_cell_count_width):
                air_score += 0.5 * self.kernel[kernel_y][kernel_x]
        wall_contribution = air_score / (kernel_cell_count_width ** 2) #make it an average
        print("air score", air_score)
        max_valid_score = float("-inf")
        kernel_center_max_valid_score = Vector2(-1, -1)
        for cell_y in range(len(self.cells) - kernel_cell_count_width):
            for cell_x in range(len(self.cells[cell_y]) - kernel_cell_count_width):
                score = 0
                for kernel_y in range(kernel_cell_count_width):
                    for kernel_x in range(kernel_cell_count_width):
                        cell = self.cells[cell_y + kernel_y][cell_x + kernel_x]
                        if cell.is_wall: score += wall_contribution
                        else: score += cell.weight * self.kernel[kernel_y][kernel_x]
                #print("score: ", score, cell_y, cell_x)
                if score > air_score + self.BOTTLE_DETECTION_MIN_SCORE_OVER_AIR and score > max_valid_score:
                    max_valid_score = score
                    kernel_center_max_valid_score = Vector2(cell_x + kernel_cell_count_width / 2, cell_y + kernel_cell_count_width / 2)
        print("max valid score: ", max_valid_score, kernel_center_max_valid_score)
        return kernel_center_max_valid_score
                    

    #can only get it to work when diameter of bottle is even number
    def create_kernel(self, canvas, should_draw = False):
        def normal_round(n):
            if n - math.floor(n) < 0.5:
                return math.floor(n)
            return math.ceil(n)

        kernel_cell_count_exact = 2 * self.KERNEL_BORDER_CM + \
            self.BOTTLE_DIAMETER_CM / self.spacing_cm
        kernel_cell_count = normal_round(kernel_cell_count_exact)
        kernel = []
        bottle_radius = (kernel_cell_count_exact / 2) - self.KERNEL_BORDER_CM
        # print("lentgth; ", kernel_cell_count_exact,
            #   kernel_cell_count, bottle_radius)
        kernel_center = Vector2(
            kernel_cell_count_exact / 2, kernel_cell_count_exact / 2)
        # print("center: ", kernel_center.x, kernel_center.y)
        for y in range(kernel_cell_count):
            kernel.append([])
            for x in range(kernel_cell_count):
                real_cell_x = x + (kernel_cell_count_exact /
                                   kernel_cell_count) / 2
                real_cell_y = y + (kernel_cell_count_exact /
                                   kernel_cell_count) / 2
                dist_from_kernel_center = math.sqrt((
                    kernel_center.x - real_cell_x) ** 2 + (kernel_center.y - real_cell_y) ** 2)
                if dist_from_kernel_center <= bottle_radius:
                    kernel[y].append(1)
                elif dist_from_kernel_center > bottle_radius and dist_from_kernel_center < bottle_radius + self.KERNEL_IGNORE_BORDER_CM:
                    kernel[y].append(0)
                else:
                    kernel[y].append(-1)
        self.kernel = kernel

        # # draw test
        if should_draw:
            particles = []
            for y in range(len(kernel)):
                for x in range(len(kernel[y])):
                    particles.append(CellOccupancyMap(
                        x * self.spacing_cm + 100, y * self.spacing_cm + 100, (kernel[y][x] + 1) / 2, False))
            canvas.drawParticles(particles)
