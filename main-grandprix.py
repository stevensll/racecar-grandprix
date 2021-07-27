### BWSI 2021 Grandprix Team CocaCola
#newtest
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

#VARIABLES GO HERE

RIGHT_WINDOW = (32,38)
LEFT_WINDOW = (322,328)
timer = 0.0

MIN_CONTOUR_AREA = 30

# A crop window for the floor directly in front of the car
CROP_FLOOR = ((360, 0), (rc.camera.get_height(), rc.camera.get_width()))
BLUE = ((90, 50, 50), (120, 255, 255), "blue")  # The HSV range for the color blue
GREEN = ((40,50,50), (80,255,255), "green")
RED = ((170,50,50), (10,255,255), "red")
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour


def start():
    rc.drive.stop()
    print("Team Cocacola Grand Prix Challenge!")

def update():

def green_line_follow():
    global contour_center,contour_area,angle,speed,color_image,color_priority2


    color1 = None
    color2 = None
    color3 = None

    if color_image is None:
        contour_center = None
        contour_area = 0

    else:
        image = rc_utils.crop(color_image, CROP_FLOOR[0], CROP_FLOOR[1])
        blue_contours = rc_utils.find_contours(image, BLUE[0], BLUE[1])
        red_contours = rc_utils.find_contours(image, RED[0], RED[1])
        green_contours = rc_utils.find_contours(image, GREEN[0], GREEN[1])
        
        if color_priority == "blue":
            color1 = blue_contours
            color2 = green_contours
            color3 = red_contours
        elif color_priority == "red":
            color1 = red_contours
            color2 = green_contours
            color3 = blue_contours
        else:
            color1 = green_contours
            color2 = blue_contours
            color3 = red_contours

        if rc_utils.get_largest_contour(color1, MIN_CONTOUR_AREA) is not None:
            contours = color1
        elif rc_utils.get_largest_contour(color2, MIN_CONTOUR_AREA) is not None:
            contours = color2
        elif rc_utils.get_largest_contour(color3, MIN_CONTOUR_AREA) is not None:
            contours = color3
        else:
            contours = [] 
        contour = rc_utils.get_largest_contour(contours, MIN_CONTOUR_AREA)
        if contour is not None:
            contour_center = rc_utils.get_contour_center(contour)
            contour_area = rc_utils.get_contour_area(contour)
            rc_utils.draw_contour(image, contour)
            rc_utils.draw_circle(image, contour_center)
        else:
            contour_center = None
            contour_area = 0

    rc.display.show_color_image(image)






if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
