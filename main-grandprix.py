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
import custom_funcs as rc_cf


rc = racecar_core.create_racecar()
class State(IntEnum) :
    challenge1 = 1
    challenge2 = 2

#VARIABLES GO HERE


########################################################################################
# CONSTANTS
########################################################################################


# Color HSV
CROP_FLOOR = ((360, 0), (rc.camera.get_height(), rc.camera.get_width()))
BLUE = ((90, 200, 200), (120, 255, 255), "blue")  
GREEN = ((40,50,50), (80,255,255), "green")
RED = ((170,50,50), (10,255,255), "red")

RIGHT_WINDOW = (32,38)
LEFT_WINDOW = (322,328)
timer = 0.0

MIN_CONTOUR_AREA = 30

speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels



def start():
    rc.drive.stop()
    print("Team Cocacola Grand Prix Challenge!")

def update():
    global speed
    global angle
    image = rc.camera.get_color_image()
    # green_center,green_area,green_image = rc_cf.get_contour_info(image, GREEN[0], GREEN[1], CROP_FLOOR)
    # rc.display.show_color_image(green_image)

    # angle  = rc_utils.remap_range(green_center[1],0, rc.camera.get_width(), -1,1, True)
    
    speed = 1
   
   
    rc.drive.set_speed_angle(speed, angle)
    
    if rc.controller.is_down(rc.controller.Button.B):
        print(speed)
        # if green_center is None:
        #     print("No green contour found")
        # else:
        #     print(green_center, speed)



if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
