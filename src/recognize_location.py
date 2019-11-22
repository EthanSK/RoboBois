import movement
import sensor
import robot
import brickpi3
import time
import montecarlo
from vector2 import Vector2
from particleDataStructures import Particles, canvas, Particle
import random
import place_recog
from main import roboboi


try:
    signatures = place_recog.SignatureContainer(5)

    input("set in location to guess (Press Enter when ready)")
    res = place_recog.recognize_location(roboboi, signatures, True)
    # print("location index: ", res[0], "angle shift: ", res[1])
    # while True:
    #     dist = roboboi.sensor_module.get_sonar_distance()
    #     print(dist)

    roboboi.reset()

except KeyboardInterrupt:
    roboboi.reset()
