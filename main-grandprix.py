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
CROP_FLOOR = ((300, 0), (rc.camera.get_height(), rc.camera.get_width()))

BLUE = ((90, 200, 200), (120, 255, 255), "blue")  
GREEN = ((40,50,50), (80,255,255), "green")
RED = ((170,50,50), (10,255,255), "red")
ORANGE = ((15,230,230), (35,255,255,),"orange")
PURPLE = ((125,200,200),(140,255,255), "purple")


RIGHT_WINDOW = (32,38)
LEFT_WINDOW = (322,328)
timer = 0.0

MIN_CONTOUR_AREA = 30

speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels

right_center = [0,0]
left_center = [0,0]


def start():
    rc.drive.stop()
    print("Team Cocacola Grand Prix Challenge!")

def update():
    global speed
    global angle
    global right_center
    global left_center
    image = rc.camera.get_color_image()

    color = PURPLE  
    turn_priority = "PURPLE"
    
    cropped_image = rc_utils.crop(image, CROP_FLOOR[0], CROP_FLOOR[1])

    purple_contours = rc_utils.find_contours(cropped_image, PURPLE[0], PURPLE[1])
    orange_contours = rc_utils.find_contours(cropped_image, ORANGE[0], ORANGE[1])
    
    # if purple_contours:
    #     purple_area = rc_utils.get_contour_area(rc_utils.get_largest_contour(purple_contours, MIN_CONTOUR_AREA))
    # else: 
    #     purple_area = 0
    
    # if orange_contours:
    #     orange_area = rc_utils.get_contour_area(rc_utils.get_largest_contour(orange_contours, MIN_CONTOUR_AREA))
    # else:
    #     orange_area = 0

    if turn_priority == "PURPLE":
        if purple_contours: 
            print("purple")
            rc_utils.draw_contour(cropped_image, purple_contours[0])
            color = PURPLE
        else: 
            color = ORANGE




    contours = rc_cf.get_n_contour_info(2,image,color[0],color[1], CROP_FLOOR)
    


    if contours is not None:
        print(len(contours))
        if len(contours) >= 1:
            if contours[0] is not None and contours[0][1] is not None:
                right_center = contours[0][1]

        if len(contours) == 2:
            if contours [1] is not None and contours[1][1] is not None:
                left_center = contours[1][1]
                
    center = [(right_center[0] + left_center[0]) // 2, (right_center[1] + left_center[1])//2]

    rc_utils.draw_circle(cropped_image, left_center)
    rc_utils.draw_circle(cropped_image, right_center)
    rc_utils.draw_circle(cropped_image, center)



    rc.display.show_color_image(cropped_image)

    
    
    
    
    lt = rc.controller.Trigger.LEFT
    rt = rc.controller.Trigger.RIGHT
    
    speed = rc.controller.get_trigger(rt)-rc.controller.get_trigger(lt)
    angle = rc.controller.get_joystick(rc.controller.Joystick.LEFT)[0]
    
    speed = 0.5
    angle = rc_utils.remap_range(center[1],0,rc.camera.get_width(),-1,1,True)

    rc.drive.set_speed_angle(speed, angle)
    if rc.controller.is_down(rc.controller.Button.B):
        print(angle)
        # if green_center is None:
        #     print("No green contour found")
        # else:
        #     print(green_center, speed)
    
if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
