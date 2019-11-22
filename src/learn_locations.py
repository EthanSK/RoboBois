

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
    signatures.delete_loc_files()  # delete from previous runs

    input("set location 1 (Press Enter when ready)")
    place_recog.learn_location(roboboi, signatures)
    input("set location 2 (Press Enter when ready)")
    place_recog.learn_location(roboboi, signatures)
    input("set location 3 (Press Enter when ready)")
    place_recog.learn_location(roboboi, signatures)
    input("set location 4 (Press Enter when ready)")
    place_recog.learn_location(roboboi, signatures)
    input("set location 5 (Press Enter when ready)")
    place_recog.learn_location(roboboi, signatures)

    roboboi.reset()

except KeyboardInterrupt:
    roboboi.reset()
