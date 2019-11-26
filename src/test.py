import movement
import sensor
import robot
import brickpi3
import time
import montecarlo
from vector2 import Vector2
from particleDataStructures import Particles, canvas, Particle
import random
from main import roboboi

try:
    #res = roboboi.movement_module.move_linear(10, 10, roboboi, True)
    roboboi.force_pos_rot(Vector2(0, 0), 0)
    roboboi.move_to_pos(Vector2(-10, 10), 10, 45, False, True)
    while True:
        pass
        break

except KeyboardInterrupt:
    roboboi.reset()
