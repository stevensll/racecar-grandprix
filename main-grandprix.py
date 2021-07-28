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
CROP_FLOOR = ((0, 0), (rc.camera.get_height(), rc.camera.get_width()))

BLUE = ((90, 200, 200), (120, 255, 255), "blue")  
GREEN = ((40,50,50), (80,255,255), "green")
RED = ((170,50,50), (10,255,255), "red")
ORANGE = ((15,200,200), (35,255,255,),"orange")
PURPLE = ((125,50,50),(140,255,255), "purple")


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
    
    # center,area,image = rc_cf.get_contour_info(image, ORANGE[0], ORANGE[1], CROP_FLOOR)
    
    # rc.display.show_color_image(image)
    # if center is not None:
    #     angle  = rc_utils.remap_range(center[1],0, rc.camera.get_width(), -1,1, True)
    
    # speed = 1
   
    color = PURPLE  


    left_image =image[0:rc.camera.get_height(),0:rc.camera.get_width()//2]
    right_image = image[0:rc.camera.get_height(),rc.camera.get_width()//2:rc.camera.get_width()-1]

    left_line_center,area,left_cropped = rc_cf.get_contour_info(left_image, color[0],color[1],CROP_FLOOR,50)
    right_line_center,area,right_cropped = rc_cf.get_contour_info(right_image, color[0], color[1], CROP_FLOOR,50)


    # rc_utils.draw_circle(left_cropped,left_line_center)
    # rc_utils.draw_circle(right_cropped,right_line_center)
    cropped_image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])

    if left_line_center or right_line_center is not None:
        right_line_center[1]+=rc.camera.get_width()//2
        center = [(left_line_center[0] + right_line_center[0] )// 2,(left_line_center[1] + right_line_center[1])// 2]
        # center = [(left_line_center[0]),(left_line_center[1] + 300)]
        rc_utils.draw_circle(cropped_image, left_line_center)
        rc_utils.draw_circle(cropped_image, right_line_center)

        rc_utils.draw_circle(cropped_image, center)
        rc.display.show_color_image(cropped_image)
        
        angle  = rc_utils.remap_range(center[1],0, rc.camera.get_width(), -1,1, True)


    speed = 0.5

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
