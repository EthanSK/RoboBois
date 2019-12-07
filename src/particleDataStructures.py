#!/usr/bin/env python

# Some suitable functions and data structures for drawing a map and particles

import time
import random
import math
import montecarlo
from vector2 import Vector2
from line import Line

# Functions to generate some dummy particles data:


def calcX():
    return random.gauss(80, 3) + 70*(math.sin(t))  # in cm


def calcY():
    return random.gauss(70, 3) + 60*(math.sin(2*t))  # in cm


def calcW():
    return random.random()


def calcTheta():
    return random.randint(0, 360)

# A Canvas class for drawing a map and particles:
# 	- it takes care of a proper scaling and coordinate transformation between
#	  the map frame of reference (in cm) and the display (in pixels)


class Canvas:
    def __init__(self, map_size=210):
        self.map_size = map_size    # in cm
        self.canvas_size = 768         # in pixels
        self.margin = 0.05*map_size
        self.scale = self.canvas_size/(map_size+2*self.margin)

    def drawLine(self, line):
        x1 = self.__screenX(line[0])
        y1 = self.__screenY(line[1])
        x2 = self.__screenX(line[2])
        y2 = self.__screenY(line[3])
        print("drawLine:" + str((x1, y1, x2, y2)))

    def draw_line_from_obj(self, line_obj):
        self.drawLine((line_obj.start_point.x, line_obj.start_point.y,
                       line_obj.end_point.x, line_obj.end_point.y))

    def drawParticles(self, data):
        display = [(self.__screenX(d.pos.x), self.__screenY(d.pos.y)) + (d.theta, d.weight)
                   for d in data]
        print("drawParticles:" + str(display))

    def __screenX(self, x):
        return (x + self.margin)*self.scale

    def __screenY(self, y):
        return (self.map_size + self.margin - y)*self.scale

# A Map class containing walls


class Map:
    def __init__(self):
        self.walls = []

    def add_wall(self, wall):
        self.walls.append(wall)

    def clear(self):
        self.walls = []

    def draw(self):
        for wall in self.walls:
            canvas.drawLine(wall)

    def convert_walls_to_lines(self):
        res = []
        for wall in self.walls:
            res.append(
                Line(Vector2(wall[0], wall[1]), Vector2(wall[2], wall[3])))
        return res
# Simple Particles set


class Particle:
    def __init__(self, x, y, theta, weight):
        self.pos = Vector2(x, y)
        self.theta = theta
        self.weight = weight


class Particles:
    def __init__(self, num_particles):
        self.count = num_particles
        self.data = []

    # this method was copied from sample
    def random_sample_data(self):
        self.data = [Particle(calcX(), calcY(), calcTheta(), calcW())
                     for i in range(self.count)]

    def init_particles(self, pos, theta):
        self.data = [Particle(pos.x, pos.y, theta, 1 / self.count)
                     for i in range(self.count)]

    def update_weights(self, sensor_distance):
        for p in self.data:
            likelihood = montecarlo.calculate_likelihood(
                p.pos.x, p.pos.y, p.theta, sensor_distance)
            p.weight = likelihood  # update weight

    def normalize_weights(self):
        acc = 0
        for p in self.data:
            acc += p.weight

        for p in self.data:
            p.weight /= acc

    def resample(self):
        cum = []
        # generate cumulative weight array
        acc = 0  # weight accumulator
        for p in self.data:
            acc += p.weight
            cum.append(acc)

        # generate <count> random numbers and create a copy of self.data[i] where i is the index of the upper bound of where the random number falls in the range of two consectutive values in the cum array
        # https://robotics.stackexchange.com/a/481
        new = []
        for i in range(self.count):
            rando = random.random()
            for j in range(len(cum)):
                if cum[j] > rando:
                    old_p = self.data[j]
                    new_p = Particle(old_p.pos.x, old_p.pos.y,
                                     old_p.theta, 1 / self.count)
                    new.append(new_p)
                    break

        self.data = new

    def draw(self):
        canvas.drawParticles(self.data)


canvas = Canvas()  # global canvas we are going to draw on

# mymap = Map()
# # Definitions of walls
# # a: O to A
# # b: A to B
# # c: C to D
# # d: D to E
# # e: E to F
# # f: F to G
# # g: G to H
# # h: H to O
# mymap.add_wall((0, 0, 0, 168))        # a
# mymap.add_wall((0, 168, 84, 168))     # b
# mymap.add_wall((84, 126, 84, 210))    # c
# mymap.add_wall((84, 210, 168, 210))   # d
# mymap.add_wall((168, 210, 168, 84))   # e
# mymap.add_wall((168, 84, 210, 84))    # f
# mymap.add_wall((210, 84, 210, 0))     # g
# mymap.add_wall((210, 0, 0, 0))        # h
# mymap.draw()

# particles = Particles()

t = 0
# while True:
#     particles.random_sample_data()
#     particles.draw()
#     t += 0.05
#     time.sleep(0.05)
