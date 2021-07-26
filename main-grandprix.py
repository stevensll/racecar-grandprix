### BWSI 2021 Grandprix Team CocaCola
import sys
from typing import Tuple
import cv2 as cv
import numpy as np
from numpy.testing._private.utils import jiffies

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils
from enum import IntEnum

rc = racecar_core.create_racecar()

class State(IntEnum) :
    challenge1 = 1
    challenge2 = 2

def start():
    rc.drive.stop()
    print("Team Cocacola Grand Prix Challenge!")

def update():





if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()